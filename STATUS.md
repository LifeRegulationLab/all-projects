# Where each project stands

Stuart Houlihan. Last updated 23 October 2026, 18:55 (Guernsey).

Checked against GitHub, App Store Connect notes from today and the folders on the Mac. Update this file at the end of any sitting that changes a build, a pull request or a TestFlight group. The Mac's evening check, [SYNC-CHECK.md](SYNC-CHECK.md), compares every folder with GitHub at 21:00 each day and says when this file has fallen behind.

## Waiting on Stuart (business)

- App Store Connect, Business page: the **W-9** tax form and the **Paid Apps Agreement** are outstanding. Paid Apps is needed before any subscription or paid app (Mull, Desk, Regulate Plus) can go on sale.

## Apps on App Store Connect

All under team PCA5FZ26HM. "Testers" is the external group (Apple reviews each new version's first build); "Internal" or "Me" is Stuart's own group (no review).

| App | Newest build | TestFlight | Repo and branch | Open PRs |
| --- | --- | --- | --- | --- |
| Pace | 0.2 (6), the Apple Watch build | 0.2 (5) in Testers, Waiting for Review. 0.2 (6) in Internal, so Stuart has it now. | pace, main | #2 Share with Coach |
| Mull | 1.0 (3), with the Apple Watch app | 1.0 (3) in Testers, Waiting for Review. Review sign-in: review@liferegulationlab.com. | mull, claude/project-thread-ni92pc (the repo's default; there is no main yet) | none |
| Desk | iOS and macOS 1.0.0 (2); iOS 1.0.0 (3) with the icon fix | iOS 1.0.0 (2) in Testers, Waiting for Review. iOS 1.0.0 (3) cannot join Testers until build 2 is approved. | Desk, main | none |
| Regulate | 0.1.0 (3), with Reset and the iPhone fixes | Internal only ("Me" group). Not for outside testers. | regulate, main | #37 Coming soon; #38 and #39 drafts (phone sign-in, RevenueCat); #40 transfers wording |
| Cairn | 1.0 (1), uploaded 23 October 12:29 | Processing on 23 October; no TestFlight groups yet. | cairn, main | none |
| Head Untangled app | 1.0 (3) | 1.0 (3) in "Testers" (external, new), Waiting for Review. Also in internal "Test". | coaching-studio, claude/project-thread-ni92pc | #5 Resets |

Merged today: Pace #5 and #6, Mull #1, Desk #7, #8 and #9, Regulate #53 and #54, Cairn #8 (iPhone and iPad app, Delete my account), liferegulationlab-site #9, #10, #11 and #12, all-projects #3, #4 and #5 (the evening sync check).

### Next steps

1. **Pace:** when Apple approves 0.2 (5), add 0.2 (6) to Testers and press Submit for Review. Try the watch app on a real watch. Next upload must be build 7 or higher.
2. **Mull:** when Apple approves 1.0 (3), testers get it. Try the watch app. Still to build: subscriptions (needs the Paid Apps Agreement). Next upload must be build 4 or higher.
3. **Desk:** when Apple approves iOS 1.0.0 (2), add iOS 1.0.0 (3) to Testers, then add macOS 1.0.0 (2) to the same group.
4. **Regulate:** stays closed to new accounts. Open privacy and data protection actions are in the Regulate status note (Claude project files/Regulate/Regulate-Status.md).
5. **Head Untangled app:** when Apple approves 1.0 (3), TestFlight emails the invitation. Decide on PR #5 (Resets).
6. **Cairn:** invite review@liferegulationlab.com as Staff on app.cairncare.app and set its password; once build 1 has processed, run the TestFlight Chrome prompt (project files, cairn/chrome-prompt-testflight-v1.md). Next upload must be build 2 or higher.

## Other projects

| Project | Where it is | State |
| --- | --- | --- |
| Cairn | cairn, main | PR #8 merged 23 October: iPhone and iPad app (no sign-up or payment in the app) and Delete my account. |
| liferegulationlab.com | liferegulationlab-site, master | Privacy page covers Pace, Mull, Desk, the Head Untangled app and Cairn (PRs #9 to #12, all merged). |
| headuntangled.com | headuntangled-site, main | PR #1 (courses page and email address) open. |
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
