# Where each project stands

Stuart Houlihan. Last updated 23 October 2026, 12:00 (Guernsey).

Checked against GitHub, App Store Connect notes from today and the folders on the Mac. Update this file at the end of any sitting that changes a build, a pull request or a TestFlight group.

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
| Head Untangled app | 1.0 (3) | Uploaded 23 October. Check which group holds it. | coaching-studio, claude/project-thread-ni92pc | #5 Resets |

Merged today: Pace #5 and #6, Mull #1, Desk #7, #8 and #9, Regulate #53 and #54, liferegulationlab-site #9 and #10.

### Next steps

1. **Pace:** when Apple approves 0.2 (5), add 0.2 (6) to Testers and press Submit for Review. Try the watch app on a real watch. Next upload must be build 7 or higher.
2. **Mull:** when Apple approves 1.0 (3), testers get it. Try the watch app. Still to build: subscriptions (needs the Paid Apps Agreement). Next upload must be build 4 or higher.
3. **Desk:** when Apple approves iOS 1.0.0 (2), add iOS 1.0.0 (3) to Testers, then add macOS 1.0.0 (2) to the same group.
4. **Regulate:** stays closed to new accounts. Open privacy and data protection actions are in the Regulate status note (Claude project files/Regulate/Regulate-Status.md).
5. **Head Untangled app:** confirm the group for 1.0 (3); decide on PR #5 (Resets).

## Other projects

| Project | Where it is | State |
| --- | --- | --- |
| Cairn | cairn, branch claude/project-thread-zjslm7 | PR #1 (DPIA pack for the hosted service) open. Last change 18 October. |
| liferegulationlab.com | liferegulationlab-site, master | Privacy page covers Pace, Mull and Desk (PRs #9, #10). |
| headuntangled.com | headuntangled-site, main | PR #1 (courses page and email address) open. |
| Voice Studio | voice-studio | Working; no change since 15 October. |
| Content engine | content-engine, main | Last change 20 October. |
| Claude Code mods | claude-mods, main | Last change 14 October. |
| Dashboards | dashboards, main | Last change 17 October. |
| Coach (private) | Claude project files/private-coach, not in git | Stuart's own app. Mull is the App Store version. |
| Ledger | Claude project files/Ledger, not in git | Personal money app, 14 October. |

## Folders on the Mac

| Folder | Repo | State on 23 October |
| --- | --- | --- |
| Desktop/regulate | regulate, claude/store-plus | Up to date. Local changes left alone: strings.xml, brand files. |
| Desktop/regulate-testflight | regulate, main at #54 (detached) | Used for Regulate 0.1.0 (3). Build output untracked. |
| Desktop/regulate-cycle | regulate (detached, 12 October) | Old cycle work with local changes. Left alone. |
| Desktop/coaching-studio | coaching-studio, claude/project-thread-ni92pc | Up to date. Xcode package changes left alone. |
| Desktop/cairn | cairn, claude/project-thread-zjslm7 | Up to date. Many untracked .cptmp copy files and a Claude outputs folder left alone. |
| Desktop/content-engine | content-engine, main | Pulled to match GitHub. |
| Desktop/claude-mods | claude-mods, main | Pulled to match GitHub. |
| Claude project files/desk-store | Desk, main | Pulled to match GitHub (#9). |
| Claude project files/mull | mull, claude/project-thread-ni92pc | Pulled to match GitHub (watch app). |
| Claude project files/mull-watch-build | mull, claude/project-thread-pd8soh | Merged branch; build logs only. |
| Claude project files/Voice Studio | voice-studio, claude/project-thread-2529dx | Up to date. |
| Claude project files/pace/build | pace, several copies | Build snapshots named after commits. None is on current main; pace-75e96d1 is 30 commits behind. |

No local copy: dashboards, headuntangled-site, liferegulationlab-site, formulationassistant-site.
