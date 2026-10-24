#!/usr/bin/env python3
"""Evening sync check for the Life Regulation Lab projects.

Looks at every git folder on the Mac, compares it with GitHub, brings a
folder up to date only when that is safe (no changed files, nothing of its
own to merge), copies the project files folder into Google Drive, and
writes SYNC-CHECK.md in this repo. It never deletes,
pushes code, merges or changes a branch. The only thing it pushes is
SYNC-CHECK.md itself.

Run by hand:   python3 ~/all-projects/tools/sync-check.py
Options:       --no-update   report only, change no folder
               --no-push     write SYNC-CHECK.md but do not commit or push it
               --no-notify   no Mac notification

Author: Stuart Houlihan
"""

import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

HOME = os.path.expanduser("~")
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(REPO_DIR, "SYNC-CHECK.md")
STATUS = os.path.join(REPO_DIR, "STATUS.md")
OWNER = "LifeRegulationLab"

# Where to look for project folders, and how deep.
ROOTS = [os.path.join(HOME, "Desktop"), REPO_DIR]
MAX_DEPTH = 4
SKIP_NAMES = {
    "node_modules", "Pods", "build", "DerivedData", "_to_delete", ".build",
    "dist", ".next", "venv", ".venv", "__pycache__", "Library",
}
ICLOUD = os.path.join(HOME, "Library", "Mobile Documents", "com~apple~CloudDocs")
CLOUD_STORAGE = os.path.join(HOME, "Library", "CloudStorage")

# Copied to Google Drive each evening. Git folders inside are left out (GitHub holds them),
# and so are build output and anything waiting to be binned.
BACKUP_SOURCE = os.path.join(HOME, "Desktop", "Claude project files")
BACKUP_FOLDER = "Mac backup"
BACKUP_SKIP = ["Tautenay and HSC", "_to_delete", "build", "DerivedData", "node_modules", "Pods", ".build", ".DS_Store"]

# launchd starts with a bare PATH; gh lives under Homebrew.
os.environ["PATH"] = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:" + os.environ.get("PATH", "")
os.environ["GIT_TERMINAL_PROMPT"] = "0"


def run(args, cwd=None, timeout=120):
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, "", str(e)


def git(path, *args, timeout=120):
    return run(["git", "-C", path] + list(args), timeout=timeout)


def short(path):
    for root, label in ((os.path.join(HOME, "Desktop"), "Desktop"), (HOME, "~")):
        if path == root:
            return label
        if path.startswith(root + os.sep):
            return label + "/" + path[len(root) + 1:]
    return path


def find_repos():
    found, denied = [], []
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        stack = [(root, 0)]
        while stack:
            path, depth = stack.pop()
            if os.path.exists(os.path.join(path, ".git")):
                found.append(path)
                continue  # do not look inside a repo for more repos
            if depth >= MAX_DEPTH:
                continue
            try:
                entries = sorted(os.scandir(path), key=lambda e: e.name)
            except PermissionError:
                denied.append(path)
                continue
            except OSError:
                continue
            for e in entries:
                if e.name.startswith(".") or e.name in SKIP_NAMES or e.name.endswith(".app"):
                    continue
                try:
                    if e.is_dir(follow_symlinks=False):
                        stack.append((e.path, depth + 1))
                except OSError:
                    pass
    # one entry per real folder
    seen, out = set(), []
    for p in found:
        rp = os.path.realpath(p)
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return sorted(out, key=lambda p: short(p).lower()), denied


def counts(path, a, b):
    """Commits only in a, commits only in b."""
    code, out, _ = git(path, "rev-list", "--left-right", "--count", "%s...%s" % (a, b))
    if code != 0 or not out:
        return None
    left, right = out.split()
    return int(left), int(right)


def remote_name(url):
    name = url.rstrip("/").split("/")[-1]
    return name[:-4] if name.endswith(".git") else name


def check_repo(path, update):
    r = {"path": path, "label": short(path), "needs": [], "notes": [], "updated": None}
    _, url, _ = git(path, "remote", "get-url", "origin")
    r["remote"] = remote_name(url) if url else ""
    if not url:
        r["needs"].append("is not linked to GitHub, so nothing in it is backed up there")
        r["branch"] = git(path, "rev-parse", "--abbrev-ref", "HEAD")[1]
        r["state"] = "no GitHub link"
        return r

    code, _, err = git(path, "fetch", "--quiet", "origin", timeout=180)
    if code != 0:
        r["needs"].append("could not reach GitHub (%s)" % (err.splitlines()[-1] if err else "no reason given"))

    _, branch, _ = git(path, "rev-parse", "--abbrev-ref", "HEAD")
    r["branch"] = branch
    _, last, _ = git(path, "log", "-1", "--format=%cd", "--date=format:%d %b")
    r["last"] = last

    # default branch on GitHub
    code, head, _ = git(path, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    default = head if code == 0 else ""
    if not default:
        for cand in ("origin/main", "origin/master"):
            if git(path, "rev-parse", "--verify", "--quiet", cand)[0] == 0:
                default = cand
                break
    r["default"] = default.replace("origin/", "")

    # changed and new files
    _, status, _ = git(path, "status", "--porcelain")
    lines = [l for l in status.splitlines() if l]
    changed = [l for l in lines if not l.startswith("??")]
    untracked = [l for l in lines if l.startswith("??")]
    r["changed"], r["untracked"] = len(changed), len(untracked)
    if changed:
        r["needs"].append("has %d changed file%s not saved to GitHub" % (len(changed), "" if len(changed) == 1 else "s"))

    state = []
    if branch == "HEAD":
        state.append("fixed copy, not on a branch")
        if default:
            c = counts(path, "HEAD", "origin/" + r["default"])
            if c and c[1]:
                r["notes"].append("fixed copy for a build; GitHub's %s is %d commit%s newer" % (r["default"], c[1], "" if c[1] == 1 else "s"))
    else:
        code, upstream, _ = git(path, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
        if code != 0:
            r["needs"].append("branch %s has never been sent to GitHub" % branch)
            state.append("not on GitHub")
        else:
            c = counts(path, "HEAD", "@{u}")
            ahead, behind = c if c else (0, 0)
            if ahead:
                r["needs"].append("has %d commit%s not sent to GitHub" % (ahead, "" if ahead == 1 else "s"))
                state.append("%d to send" % ahead)
            if behind:
                if update and not changed and not ahead:
                    code, _, err = git(path, "merge", "--ff-only", "--quiet", "@{u}")
                    if code == 0:
                        r["updated"] = behind
                        state.append("brought up to date (%d)" % behind)
                        behind = 0
                    else:
                        r["needs"].append("is %d behind GitHub and could not be brought up to date safely" % behind)
                        state.append("%d behind" % behind)
                else:
                    why = "it has changed files" if changed else ("it also has commits of its own" if ahead else "updates are off")
                    if update and changed:
                        r["needs"][0] += ", and is %d commit%s behind GitHub" % (behind, "" if behind == 1 else "s")
                    elif update:
                        r["needs"].append("is %d commit%s behind GitHub; not updated because %s" % (behind, "" if behind == 1 else "s", why))
                    state.append("%d behind" % behind)

        # other local branches holding work that is not on GitHub
        _, others, _ = git(path, "for-each-ref", "--format=%(refname:short)", "refs/heads")
        for b in others.splitlines():
            if b == branch:
                continue
            _, n, _ = git(path, "rev-list", "--count", b, "--not", "--remotes")
            if n.isdigit() and int(n):
                # nothing to lose if the branch holds exactly what GitHub's main line holds
                if default and git(path, "diff", "--quiet", "origin/" + r["default"], b)[0] == 0:
                    continue
                r["needs"].append("has %s commit%s on branch %s that %s not on GitHub" % (n, "" if n == "1" else "s", b, "is" if n == "1" else "are"))

        # working branch compared with the main line on GitHub
        if default and branch != r["default"]:
            c = counts(path, "HEAD", "origin/" + r["default"])
            if c:
                own, newer = c
                if own == 0 and newer:
                    r["needs"].append("is on branch %s, which is already merged; GitHub's %s is %d commit%s newer" % (branch, r["default"], newer, "" if newer == 1 else "s"))
                elif own:
                    r["notes"].append("working branch %s: %d commit%s not yet in %s" % (branch, own, "" if own == 1 else "s", r["default"]))
    if not state:
        state.append("level with GitHub")
    r["state"] = ", ".join(state)
    return r


def github_overview(local_remotes):
    gh = shutil.which("gh")
    if not gh:
        return None, "GitHub command line tool not found, so open pull requests were not checked."
    code, out, err = run([gh, "repo", "list", OWNER, "--limit", "200", "--json", "name,pushedAt,isArchived"])
    if code != 0:
        return None, "Could not list GitHub repos (%s)." % (err.splitlines()[-1] if err else "no reason given")
    repos = [x for x in json.loads(out or "[]") if not x.get("isArchived")]
    code, out, err = run([gh, "search", "prs", "--owner", OWNER, "--state", "open", "--limit", "100",
                          "--json", "repository,number,title,isDraft,updatedAt,url"])
    prs = json.loads(out or "[]") if code == 0 else []
    missing = sorted((x for x in repos if x["name"].lower() not in local_remotes),
                     key=lambda x: x.get("pushedAt", ""), reverse=True)
    pushed = {x["name"]: x.get("pushedAt", "") for x in repos}
    return {"prs": prs, "missing": missing, "pushed": pushed,
            "pr_error": None if code == 0 else "Could not list pull requests."}, None


def cloud_changes(root, label, since, skip=()):
    if not root or not os.path.isdir(root):
        return None, "%s folder not found." % label
    out = []
    try:
        entries = list(os.scandir(root))
    except PermissionError:
        return None, "The Mac did not allow the check to read %s (see the note at the end)." % label
    for e in entries:
        if e.name.startswith(".") or e.name in skip:
            continue
        newest = 0.0
        try:
            newest = e.stat().st_mtime
            if e.is_dir():
                for dirpath, dirnames, filenames in os.walk(e.path):
                    dirnames[:] = [d for d in dirnames if not d.startswith(".")]
                    for f in filenames:
                        if f.startswith("."):
                            continue
                        try:
                            newest = max(newest, os.stat(os.path.join(dirpath, f)).st_mtime)
                        except OSError:
                            pass
        except OSError:
            continue
        if newest >= since:
            out.append((e.name, datetime.datetime.fromtimestamp(newest)))
    return sorted(out, key=lambda x: x[1], reverse=True), None


def drive_root():
    try:
        accounts = sorted(d for d in os.listdir(CLOUD_STORAGE) if d.startswith("GoogleDrive-"))
    except OSError:
        return None
    for d in accounts:
        mine = os.path.join(CLOUD_STORAGE, d, "My Drive")
        if os.path.isdir(mine):
            return mine
    return None


def drive_backup(drive, repos):
    """One-way copy of the project files folder into Google Drive. Never removes anything."""
    if not drive:
        return "Google Drive is not signed in on the Mac, so tonight's copy was skipped.", False
    if not os.path.isdir(BACKUP_SOURCE):
        return "%s not found, so tonight's copy was skipped." % short(BACKUP_SOURCE), False
    target = os.path.join(drive, BACKUP_FOLDER, os.path.basename(BACKUP_SOURCE))
    try:
        os.makedirs(target, exist_ok=True)
    except OSError as e:
        return "Could not make the backup folder in Google Drive (%s)." % e, False
    args = ["rsync", "-a"]
    for name in BACKUP_SKIP:
        args += ["--exclude", name]
    for r in repos:
        if r.startswith(BACKUP_SOURCE + os.sep):
            args += ["--exclude", "/" + os.path.relpath(r, BACKUP_SOURCE)]
    args += [BACKUP_SOURCE + "/", target + "/"]
    code, _, err = run(args, timeout=3 * 3600)
    if code != 0:
        return "The copy to Google Drive did not finish (%s)." % (err.splitlines()[-1] if err else "no reason given"), False
    return "Copied %s to Google Drive, My Drive/%s (git folders, build output and the Tautenay and HSC folder left out)." % (short(BACKUP_SOURCE), BACKUP_FOLDER), True


def status_updated():
    try:
        with open(STATUS, encoding="utf-8") as f:
            for line in f:
                if "Last updated" in line:
                    return line.strip().split("Last updated", 1)[1].strip(" .:")
    except OSError:
        pass
    return None


def notify(text):
    safe = text.replace("\\", "").replace('"', "'")
    run(["osascript", "-e", 'display notification "%s" with title "Sync check"' % safe], timeout=20)


def unsaved_edits():
    """Changed files in this repo other than the report itself."""
    _, out, _ = git(REPO_DIR, "status", "--porcelain", "--untracked-files=no")
    return [l for l in out.splitlines() if l.strip() and not l.endswith("SYNC-CHECK.md")]


def refresh_self():
    """Bring this repo level with GitHub. An unsaved edit (such as STATUS.md) is never touched."""
    git(REPO_DIR, "checkout", "--", "SYNC-CHECK.md")
    if unsaved_edits():
        git(REPO_DIR, "fetch", "--quiet", timeout=180)
        return
    code, _, err = git(REPO_DIR, "pull", "--rebase", "--quiet", timeout=180)
    if code != 0:
        git(REPO_DIR, "rebase", "--abort")
        print("Could not bring all-projects up to date: %s" % err)


def send_report(message):
    """Commit SYNC-CHECK.md and push it. Returns an error message, or None."""
    if not unsaved_edits():
        git(REPO_DIR, "add", "SYNC-CHECK.md")
        code, _, _ = git(REPO_DIR, "diff", "--cached", "--quiet", "--", "SYNC-CHECK.md")
        if code == 0:
            return None
        git(REPO_DIR, "commit", "--quiet", "-m", message, "--", "SYNC-CHECK.md")
        code, _, err = git(REPO_DIR, "pull", "--rebase", "--quiet", timeout=180)
        if code != 0:
            git(REPO_DIR, "rebase", "--abort")
            return err or "could not catch up with GitHub"
        code, _, err = git(REPO_DIR, "push", "--quiet", timeout=180)
        return None if code == 0 else (err or "push refused")
    # Someone has an unsaved edit here: commit the report in a separate copy so the edit stays as it is.
    code, upstream, _ = git(REPO_DIR, "rev-parse", "--abbrev-ref", "@{u}")
    if code != 0 or "/" not in upstream:
        return "no upstream branch"
    remote, branch = upstream.split("/", 1)
    git(REPO_DIR, "fetch", "--quiet", remote, timeout=180)
    tmp = tempfile.mkdtemp(prefix="sync-check-")
    try:
        code, _, err = git(REPO_DIR, "worktree", "add", "--quiet", "--detach", tmp, upstream)
        if code != 0:
            return err or "could not make a working copy"
        shutil.copyfile(REPORT, os.path.join(tmp, "SYNC-CHECK.md"))
        code, _, _ = git(tmp, "diff", "--quiet", "--", "SYNC-CHECK.md")
        if code == 0:
            return None
        git(tmp, "commit", "--quiet", "-m", message, "--", "SYNC-CHECK.md")
        code, _, err = git(tmp, "push", "--quiet", remote, "HEAD:" + branch, timeout=180)
        return None if code == 0 else (err or "push refused")
    finally:
        git(REPO_DIR, "worktree", "remove", "--force", tmp)
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    args = set(sys.argv[1:])
    update = "--no-update" not in args
    now = datetime.datetime.now()

    # keep this repo current first, so the report lands on top of the latest STATUS.md
    if update:
        refresh_self()

    repos, denied = find_repos()
    results = [check_repo(p, update) for p in repos]

    by_remote = {}
    for r in results:
        if r.get("remote"):
            by_remote.setdefault(r["remote"].lower(), []).append(r["label"])
    gh, gh_error = github_overview(set(by_remote))
    day_ago = (now - datetime.timedelta(days=1)).timestamp()
    icloud, icloud_error = cloud_changes(ICLOUD, "iCloud Drive", day_ago)
    drive = drive_root()
    backup_line, backup_ok = drive_backup(drive, repos) if update else ("Copy to Google Drive skipped (report only).", True)
    gdrive, gdrive_error = cloud_changes(drive, "Google Drive", day_ago, skip=(BACKUP_FOLDER,))

    needs = []
    for r in results:
        for n in r["needs"]:
            needs.append("**%s** %s." % (r["label"], n))
    if gh:
        for p in gh["prs"]:
            if p.get("isDraft"):
                needs.append("**%s #%d** is a draft pull request; it should be marked ready for review." % (p["repository"]["name"], p["number"]))
    if not backup_ok:
        needs.append(backup_line)
    if denied:
        needs.append("The Mac did not let the check read: %s (see the note at the end)." % ", ".join(short(d) for d in denied))
    status_line = status_updated()
    if gh and not gh_error:
        _, status_commit, _ = git(REPO_DIR, "log", "-1", "--format=%cI", "--", "STATUS.md")
        if status_commit:
            since = datetime.datetime.fromisoformat(status_commit).astimezone(datetime.timezone.utc)
            later = []
            for name, when in gh["pushed"].items():
                if name.lower() == "all-projects" or not when:
                    continue
                if datetime.datetime.fromisoformat(when.replace("Z", "+00:00")) > since:
                    later.append(name)
            if later:
                needs.append("**STATUS.md** has not been updated since changes reached GitHub in: %s." % ", ".join(sorted(later, key=str.lower)))

    w = []
    w.append("# Sync check\n")
    w.append("Stuart Houlihan. Run %s.\n" % now.strftime("%d %B %Y, %H:%M").lstrip("0"))
    w.append("Each evening the Mac compares every project folder with GitHub, brings a folder up to date when that is safe, and writes this page. It never deletes, merges or sends code. [STATUS.md](STATUS.md) is the longer account of where each app stands%s.\n"
             % ((", last updated " + status_line) if status_line else ""))

    w.append("## Needs you\n")
    if needs:
        for n in needs:
            w.append("- " + n)
    else:
        w.append("Nothing. Every folder is level with GitHub.")
    w.append("")

    updated = [r for r in results if r["updated"]]
    if updated:
        w.append("## Brought up to date tonight\n")
        for r in updated:
            w.append("- %s: %d new commit%s from GitHub." % (r["label"], r["updated"], "" if r["updated"] == 1 else "s"))
        w.append("")

    w.append("## Every folder\n")
    w.append("| Folder | Repo | Branch | State | Changed / new files | Last commit |")
    w.append("| --- | --- | --- | --- | --- | --- |")
    for r in results:
        w.append("| %s | %s | %s | %s | %s / %s | %s |" % (
            r["label"], r.get("remote", ""), r.get("branch", ""), r["state"],
            r.get("changed", 0), r.get("untracked", 0), r.get("last", "")))
    w.append("")
    notes = [(r["label"], n) for r in results for n in r["notes"]]
    dupes = {k: v for k, v in by_remote.items() if len(v) > 1}
    if notes or dupes:
        w.append("Notes:\n")
        for label, n in notes:
            w.append("- %s: %s." % (label, n))
        for k, v in sorted(dupes.items()):
            w.append("- %s is on the Mac %d times: %s." % (k, len(v), ", ".join(v)))
        w.append("")

    w.append("## GitHub\n")
    if gh_error:
        w.append(gh_error + "\n")
    else:
        if gh["pr_error"]:
            w.append(gh["pr_error"] + "\n")
        elif gh["prs"]:
            w.append("Open pull requests:\n")
            for p in sorted(gh["prs"], key=lambda p: (p["repository"]["name"].lower(), p["number"])):
                w.append("- %s #%d: %s%s" % (p["repository"]["name"], p["number"], p["title"], " (draft)" if p.get("isDraft") else ""))
            w.append("")
        else:
            w.append("No open pull requests.\n")
        if gh["missing"]:
            w.append("On GitHub but not on the Mac:\n")
            for x in gh["missing"]:
                w.append("- %s (last change %s)" % (x["name"], x.get("pushedAt", "")[:10]))
            w.append("")

    w.append("## iCloud Drive\n")
    w.append("Desktop and Documents sync is off, so iCloud does not hold a copy of the Desktop; GitHub is the backup for project folders.\n")
    if icloud_error:
        w.append(icloud_error + "\n")
    elif icloud:
        w.append("Changed in iCloud Drive in the last day. If any of this belongs to a project, it should also be in that project's folder:\n")
        for name, when in icloud:
            w.append("- %s (%s)" % (name, when.strftime("%d %b %H:%M")))
        w.append("")
    else:
        w.append("Nothing changed in iCloud Drive in the last day.\n")

    w.append("## Google Drive\n")
    w.append(backup_line + "\n")
    if gdrive_error:
        w.append(gdrive_error + "\n")
    elif gdrive:
        w.append("Changed in Google Drive in the last day, apart from the backup. If any of this belongs to a project, it should also be in that project's folder:\n")
        for name, when in gdrive:
            w.append("- %s (%s)" % (name, when.strftime("%d %b %H:%M")))
        w.append("")
    else:
        w.append("Nothing else changed in Google Drive in the last day.\n")

    if denied or any(e and "did not allow" in e for e in (icloud_error, gdrive_error)):
        w.append("## Note\n")
        w.append("macOS asks before a background task reads the Desktop, iCloud Drive or Google Drive. If folders are missing above, open System Settings, Privacy and Security, Files and Folders, and switch on everything under Sync Check.\n")

    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(w).rstrip() + "\n")

    push_error = None
    if "--no-push" not in args:
        push_error = send_report("Sync check %s" % now.strftime("%d %b %Y"))
        if push_error:
            print("Could not send SYNC-CHECK.md to GitHub: %s" % push_error)

    if "--no-notify" not in args:
        if push_error:
            notify("The report was written on the Mac but could not be sent to GitHub. See ~/Library/Logs/sync-check.log.")
        elif needs:
            notify("%d thing%s need%s you. Open SYNC-CHECK.md in all-projects." % (len(needs), "" if len(needs) == 1 else "s", "s" if len(needs) == 1 else ""))
        else:
            notify("All project folders are level with GitHub.")

    print("Wrote %s: %d folders, %d need you." % (REPORT, len(results), len(needs)))


if __name__ == "__main__":
    main()
