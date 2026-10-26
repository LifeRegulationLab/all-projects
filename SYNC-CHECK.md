# Sync check

Stuart Houlihan. Run 26 October 2026, 07:31.

Each evening the Mac compares every project folder with GitHub, brings a folder up to date when that is safe, and writes this page. It never deletes, merges or sends code. [STATUS.md](STATUS.md) is the longer account of where each app stands, last updated 23 October 2026, 19:45 (Guernsey).

## Needs you

- **/home/user/all-projects** has 1 changed file not saved to GitHub.
- Google Drive is not signed in on the Mac, so tonight's copy was skipped.

## Every folder

| Folder | Repo | Branch | State | Changed / new files | Last commit |
| --- | --- | --- | --- | --- | --- |
| /home/user/all-projects | all-projects | claude/project-thread-1fqzf1 | level with GitHub | 1 / 0 | 26 Oct |

## GitHub

Could not list GitHub repos (HTTP 403: GitHub GraphQL is not available from Claude Code sessions; use the REST API (gh api repos/{owner}/{repo}/...). For review threads, auto-merge, and draft/ready-for-review use the CCR routes on api.github.com: GET /repos/{owner}/{repo}/pulls/{n}/ccr/review_threads, POST /repos/{owner}/{repo}/pulls/{n}/ccr/comments/{comment_id}/resolve (or /unresolve), PUT or DELETE /repos/{owner}/{repo}/pulls/{n}/ccr/auto_merge, POST /repos/{owner}/{repo}/pulls/{n}/ccr/ready_for_review, POST /repos/{owner}/{repo}/pulls/{n}/ccr/convert_to_draft. (https://api.github.com/graphql)).

## iCloud Drive

Desktop and Documents sync is off, so iCloud does not hold a copy of the Desktop; GitHub is the backup for project folders.

iCloud Drive folder not found.

## Google Drive

Google Drive is not signed in on the Mac, so tonight's copy was skipped.

Google Drive folder not found.

## Cloudflare R2

rclone is not installed, so the copy to Cloudflare R2 was skipped.

rclone is not installed, so nothing was brought down from Cloudflare R2.
