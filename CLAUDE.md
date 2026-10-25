# All projects (index repo)

This repo holds no code. It is a map of the Life Regulation Lab projects; see `README.md` for the list.

When this repo is linked in a conversation:

- Treat the repos in `README.md` as the user's full set of projects.
- Add only the repos the task needs (with `add_repo`), not all of them. Each repo's own `CLAUDE.md` takes precedence for work inside it.
- When a project is added, renamed or retired, update `README.md` here.
- Before saying where a project stands, read `SYNC-CHECK.md` (the Mac's evening check against GitHub) as well as `STATUS.md`.
- Project files that are not in GitHub (video, audio, pictures, workbook PDFs and Word files, notes) are in the Cloudflare R2 bucket `lrl-media`: each evening the Mac uploads `Desktop/Projects/Head-Untangled` to `lrl-media/Head-Untangled/`, the rest of `Desktop/Projects` to `lrl-media/Projects/`, `Desktop/Claude project files` to `lrl-media/Claude project files/` and `Desktop/Channel pictures` to `lrl-media/Channel pictures/`. Look there before saying a Desktop file can't be reached. A cloud session reaches it with `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` and `R2_ENDPOINT` from the environment (S3 API, region `auto`). Save anything made in the cloud under `lrl-media/from-cloud/`; the Mac brings it down to `Desktop/From cloud` that evening. Never delete or overwrite anything outside `lrl-media/from-cloud/`.
- Brand files (logos, app icons, banners) for every project, newest first: `lrl-media/Claude project files/Life Regulation Lab/branding/` (the Life Regulation Lab logo and banner, and `app-icons/` with the current icon for every app), `lrl-media/Claude project files/<Project>/branding/` (or `Regulate/brand/`), `lrl-media/Head-Untangled/brand/<date>/` and `lrl-media/Channel pictures/`. Use these rather than asking for them, and check the date folders for the newest set.

## Filing on the Mac

Only four Desktop folders reach the cloud. A file anywhere else stays on the Mac, so file it before the evening copy at 21:00.

| What it is | Where it goes |
| --- | --- |
| Notes, specs, plans, Word and Excel documents, brand files for a project | `Desktop/Claude project files/<Project>/` (brand in `branding/`) |
| Production material: video, audio, workbooks, courses, printables, site drafts | `Desktop/Projects/<Project>/` (Head Untangled is `Desktop/Projects/Head-Untangled/`, the kit) |
| YouTube channel art | `Desktop/Channel pictures/` |
| Code | its own GitHub repo, listed in `README.md` |
| Passwords, keys, account details | `Desktop/Private - not in cloud/`, never in the folders above |
| Tautenay, HSC, QI project, Structured Care | `Desktop/Claude project files/Tautenay and HSC/` or outside these folders; never copied to the cloud and never mixed into another project's folder |
| Something to bin | `_to_delete/` next to it (left out of every copy) |

- Use the project's existing folder name; make a new `<Project>/` folder only for a new project, and add it to `README.md`.
- Name dated sets `<what>-YYYY-MM-DD` (for example `brand/2026-10-24/`) so the newest is easy to find.
- Files saved from the cloud arrive in `Desktop/From cloud`. Move each one into its project folder above; that folder is not copied back up.
- Never leave project files loose on the Desktop or in Downloads.
