# All projects

Index of Life Regulation Lab projects. Link this repo in a conversation to give Claude the full project map.

Where each project stands (builds, TestFlight, open pull requests, next steps) is in [STATUS.md](STATUS.md).

[SYNC-CHECK.md](SYNC-CHECK.md) is written by the Mac every evening at 21:00: it compares every project folder with GitHub, brings a folder up to date when that is safe, and lists only what is out of step. The check is `tools/sync-check.py`; `tools/install-sync-check.sh` sets the evening run (add `--remove` to stop it). It also copies `Desktop/Claude project files` into Google Drive (My Drive/Mac backup), leaving out git folders and build output, and lists anything changed that day in iCloud Drive or Google Drive. It copies every file in `Desktop/Projects`, `Desktop/Claude project files` and `Desktop/Channel pictures` (not git folders, build output, parts, keys, or anything Tautenay, HSC, QI or Structured Care; see Filing in `CLAUDE.md`) into the Cloudflare R2 bucket `lrl-media`, so cloud sessions can reach them without the Mac; that step needs rclone with a remote named `r2`, and is skipped until it is set up. It also brings down anything cloud sessions saved in `lrl-media/from-cloud` into `Desktop/From cloud`. It never deletes, merges or sends code; the only thing it sends to GitHub is SYNC-CHECK.md.

| Repo | What it is |
| --- | --- |
| [regulate](https://github.com/LifeRegulationLab/regulate) | Regulate: capacity-aware app for late-diagnosed neurodivergent adults. |
| [cairn](https://github.com/LifeRegulationLab/cairn) | Cairn: behavioural formulation and care-planning web app for staff supporting people with behaviour that challenges. |
| [headuntangled-site](https://github.com/LifeRegulationLab/headuntangled-site) | headuntangled.com: the Head Untangled website. Static HTML, built with `build.py`, served by Cloudflare Pages. |
| [liferegulationlab-site](https://github.com/LifeRegulationLab/liferegulationlab-site) | Life Regulation Lab website (Next.js). |
| [formulationassistant-site](https://github.com/LifeRegulationLab/formulationassistant-site) | formulationassistant.com: production site for Formulation Assistant (Astro + Tailwind, Cloudflare Pages). |
| [coaching-studio](https://github.com/LifeRegulationLab/coaching-studio) | Head Untangled app: self-coaching app (Vite, React, Capacitor) with themes, workbooks, plan, pocket card and PDF/.docx reports. |
| [voice-studio](https://github.com/LifeRegulationLab/voice-studio) | Voice Studio: local narration and video for Head Untangled, coaching app lessons and Cairn Notes, uploaded to YouTube as private. |
| [Desk](https://github.com/LifeRegulationLab/Desk) | Desk: Stuart's own office app for documents, spreadsheets, slides, PDFs, tasks, databases and drawings, using normal Microsoft file formats. |
| [dashboards](https://github.com/LifeRegulationLab/dashboards) | Personal dashboard (iPhone and Mac web app) for YouTube, Shopify and Stripe numbers, replacing vidIQ and a paid Shopify plan. |
| [pace](https://github.com/LifeRegulationLab/pace) | Pace: day planner and focus timer for iPhone, iPad, Mac and Apple Watch. |
| [mull](https://github.com/LifeRegulationLab/mull) | Mull: self-coaching app for iPhone, Mac and Apple Watch (App Store version of Stuart's private Coach). |
| [mull › Moss/](https://github.com/LifeRegulationLab/mull/tree/claude/project-thread-ni92pc/Moss) | Moss: the shared companion for the apps (Mull's face). Character, shared server tables and privacy rules; in Mull and Pace so far. |
| [head-untangled-kit](https://github.com/LifeRegulationLab/head-untangled-kit) | The Head Untangled kit folder: rules, runbook and production material (Desktop/Projects/Head-Untangled). |
| [content-engine](https://github.com/LifeRegulationLab/content-engine) | Concept to product: research, script, narrate, animate and publish videos, workbooks and courses. |
| [claude-mods](https://github.com/LifeRegulationLab/claude-mods) | Claude Code mods: auto-model, background-board, clean-view, context-gauge, cost-meter, dashboard, morning-brief, production-tracker, usage-limits. |
| [LifeRegulationLab](https://github.com/LifeRegulationLab/LifeRegulationLab) | GitHub org profile repo. |

Each repo has its own `CLAUDE.md` with its working rules; read that before changing anything in it.

Keep this table current when a project is added, renamed or retired.
