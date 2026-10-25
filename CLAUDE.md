# All projects (index repo)

This repo holds no code. It is a map of the Life Regulation Lab projects; see `README.md` for the list.

When this repo is linked in a conversation:

- Treat the repos in `README.md` as the user's full set of projects.
- Add only the repos the task needs (with `add_repo`), not all of them. Each repo's own `CLAUDE.md` takes precedence for work inside it.
- When a project is added, renamed or retired, update `README.md` here.
- Before saying where a project stands, read `SYNC-CHECK.md` (the Mac's evening check against GitHub) as well as `STATUS.md`.
- Media (video, audio, pictures) is not in GitHub. Copies are in the Cloudflare R2 bucket `lrl-media`: the Mac uploads `Desktop/Projects/Head-Untangled` to `lrl-media/Head-Untangled/` each evening. A cloud session reaches it with `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` and `R2_ENDPOINT` from the environment (S3 API, region `auto`). Save anything made in the cloud under `lrl-media/from-cloud/`; the Mac brings it down to `Desktop/From cloud` that evening. Never delete or overwrite in `lrl-media/Head-Untangled/`.
