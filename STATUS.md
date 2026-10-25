# Where each project stands

Stuart Houlihan. Last updated 23 October 2026, 19:45 (Guernsey).

Checked against GitHub, App Store Connect notes from today and the folders on the Mac. Update this file at the end of any sitting that changes a build, a pull request or a TestFlight group. The Mac's evening check, [SYNC-CHECK.md](SYNC-CHECK.md), compares every folder with GitHub at 21:00 each day and says when this file has fallen behind.

## Waiting on Stuart (business)

- App Store Connect, Business page: the **W-9** tax form and the **Paid Apps Agreement** are outstanding. Paid Apps is needed before any subscription or paid app (Mull, Regulate Plus) can go on sale.
- Desk is a personal app (Stuart, 25 Oct): it stays in TestFlight for Stuart only, never goes on sale or on any website.

## Before any app goes to App Store review or Google Play

- Check every app offers **Sign in with Apple** and **Sign in with Google** where it has an account. Not all do yet (Stuart, 25 October 2026). Apple requires Sign in with Apple when an app offers another sign-in such as Google. Check each app's sign-in screen on a phone before it is submitted.

## Apps on App Store Connect

All under team PCA5FZ26HM. "Testers" is the external group (Apple reviews each new version's first build); "Internal" or "Me" is Stuart's own group (no review).

| App | Newest build | TestFlight | Repo and branch | Open PRs |
| --- | --- | --- | --- | --- |
| Pace | 0.2 (6), the Apple Watch build | Approved. 0.1 (1), 0.2 (5) and 0.2 (6) all Testing in Testers (23 Oct evening). | pace, main | #2 Share with Coach |
| Mull | 1.0 (3), with the Apple Watch app | Approved. 1.0 (3) Testing in Testers. Review sign-in: review@liferegulationlab.com. | mull, claude/project-thread-ni92pc (the repo's default; there is no main yet) | none |
| Desk | iOS and macOS 1.0.0 (2); iOS 1.0.0 (3) with the icon fix | Approved. iOS 1.0.0 (2), iOS 1.0.0 (3) and macOS 1.0.0 (2) all Testing in Testers. | Desk, main | none |
| Regulate | 0.1.0 (3), with Reset and the iPhone fixes | Internal only ("Me" group). Not for outside testers. | regulate, main | #37 Coming soon; #38 and #39 drafts (phone sign-in, RevenueCat); #40 transfers wording |
| Cairn | 1.0 (1), uploaded 23 October 12:29 | Submitted 23 Oct evening to the external "Testers" group, Waiting for Review. | cairn, main | #1 DPIA pack |
| Head Untangled app | 1.0 (3) | Approved. 1.0 (3) Testing in "Testers". Also in internal "Test". | coaching-studio, claude/project-thread-ni92pc | #5 Resets |

Merged today: Pace #5 and #6, Mull #1, Desk #7, #8 and #9, Regulate #53 and #54, Cairn #8 (iPhone and iPad app, Delete my account), liferegulationlab-site #9, #10, #11 and #12, all-projects #3, #4 and #5 (the evening sync check).

### Next steps

1. **Cairn:** wait for Beta App Review of 1.0 (1). If Apple asks for a demo login, finish the review@liferegulationlab.com account in Willow House and add it to the Test Information. Next upload must be build 2 or higher.
2. **Pace:** try the watch app on a real watch. Check the 0.2 (6) What to Test text (written as a guess). Next upload must be build 7 or higher.
3. **Mull:** try the watch app. Subscriptions still need the Paid Apps Agreement. Next upload must be build 4 or higher.
4. **Desk:** nothing waiting.
5. **Regulate:** stays closed to new accounts. Open privacy and data protection actions are in the Regulate status note (Claude project files/Regulate/Regulate-Status.md).
6. **Head Untangled app:** testers have 1.0 (3). Decide on PR #5 (Resets).

## Other projects

| Project | Where it is | State |
| --- | --- | --- |
| Cairn | cairn, main | PR #8 merged 23 October: iPhone and iPad app (no sign-up or payment in the app) and Delete my account. |
| liferegulationlab.com | liferegulationlab-site, master | 25 October (PR #14, merged): home and Apps pages list every app with the new icons (Pace, Mull, Head Untangled app in testing; Dealt With, Whole Story in development; Cairn). Privacy covers Pace, Mull, the Head Untangled app and Cairn (Desk removed 25 Oct, PR #16, as it is personal); Dealt With and Whole Story still need entries before they reach testers. Status lines live in `src/lib/apps.ts`. |
| headuntangled.com | headuntangled-site, main | 25 October (PR #3, merged): new /app/ page for the Head Untangled app, a home page section and an App nav link. PR #1 (courses page) still open. |
| Voice Studio | voice-studio | Working; no change since 15 October. |
| Content engine | content-engine, main | 23 October: design and stage 1 plan for Head Untangled Studio, the app that queues and reviews products. |
| Head Untangled kit | head-untangled-kit, main | New repo 23 October for the kit folder (Desktop/Projects/Head-Untangled). |
| Claude Code mods | claude-mods, main | Last change 14 October. |
| Dashboards | dashboards, main | Last change 17 October. |
| Coach (private) | Claude project files/private-coach, not in git | Stuart's own app. Mull is the App Store version. |
| Ledger | Claude project files/Ledger, not in git | Personal money app, 14 October. |

## Folders on the Mac

| Folder | Repo | State on 23 October |
| --- | --- | --- |
| Desktop/regulate | regulate, claude/store-plus | Up to date and clean. Brand files moved to Claude project files/Regulate/brand. |
| Desktop/regulate-testflight | regulate, main at #54 (detached) | Used for Regulate 0.1.0 (3). Build output untracked. |
| Desktop/coaching-studio | coaching-studio, claude/project-thread-ni92pc | Up to date. Xcode raised the minimum iOS to 17; save that with the next Head Untangled build. |
| Desktop/cairn | cairn, main | Up to date (moved back to main 23 October). Claude outputs folder untracked. |
| Claude project files/Cairn/cairn-app | cairn, main | Up to date. Xcode raised the minimum iOS to 16; save that with the next Cairn build. |
| Desktop/content-engine | content-engine, main | Up to date. |
| Desktop/Projects/Head-Untangled | head-untangled-kit, main | Up to date. |
| Desktop/claude-mods | claude-mods, main | Up to date. |
| Claude project files/desk-store | Desk, main | Up to date. |
| Claude project files/mull | mull, claude/project-thread-ni92pc | Up to date (watch app). |
| Claude project files/mull-watch-build | mull, claude/project-thread-ni92pc | Build copy; build logs only. |
| Claude project files/Voice Studio | voice-studio, claude/project-thread-2529dx | Up to date. |
| Claude project files/pace/pace | pace, main | Current Pace code. Use this for new Pace builds. |
| Claude project files/pace/build | pace | Archives, plus pace-0.2 and pace-watch-6bf853d (the copies behind builds 4 and 5). |
| Claude project files/dashboards | dashboards, main | Up to date. |
| Claude project files/headuntangled-site | headuntangled-site, main | Up to date. |
| Claude project files/liferegulationlab-site | liferegulationlab-site, master | Up to date. |

Desktop/regulate also has a leftover branch, reset-merge-check, whose content is already in main; it is checked out in an old scratch copy under /private/tmp and can go when convenient.

Waiting in Desktop/_to_delete for Stuart to bin: regulate-cycle (old cycle copy; its work is in main) and cairn-copy-leftovers (empty files from an interrupted copy on 9 October). Old Pace builds (about 14 GB) are in Claude project files/pace/build/_to_delete.

Not on the Mac: formulationassistant-site (no change since April).
