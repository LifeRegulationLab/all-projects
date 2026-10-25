# All projects (index repo)

This repo holds no code. It is a map of the Life Regulation Lab projects; see `README.md` for the list.

When this repo is linked in a conversation:

- Treat the repos in `README.md` as the user's full set of projects.
- Add only the repos the task needs (with `add_repo`), not all of them. Each repo's own `CLAUDE.md` takes precedence for work inside it.
- When a project is added, renamed or retired, update `README.md` here.
- Before saying where a project stands, read `SYNC-CHECK.md` (the Mac's evening check against GitHub) as well as `STATUS.md`.
- Project files that are not in GitHub (video, audio, pictures, workbook PDFs and Word files, notes) are in the Cloudflare R2 bucket `lrl-media`: each evening the Mac uploads `Desktop/Projects/Head-Untangled` to `lrl-media/Head-Untangled/` and `Desktop/Claude project files` to `lrl-media/Claude project files/`. Look there before saying a Desktop file can't be reached. A cloud session reaches it with `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` and `R2_ENDPOINT` from the environment (S3 API, region `auto`). Save anything made in the cloud under `lrl-media/from-cloud/`; the Mac brings it down to `Desktop/From cloud` that evening. Never delete or overwrite anything outside `lrl-media/from-cloud/`.
