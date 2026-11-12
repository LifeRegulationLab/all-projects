# Where each project stands

Stuart Houlihan. Last updated 23 October 2026, 19:45 (Guernsey).

Checked against GitHub, App Store Connect notes from today and the folders on the Mac. Update this file at the end of any sitting that changes a build, a pull request or a TestFlight group. The Mac's evening check, [SYNC-CHECK.md](SYNC-CHECK.md), compares every folder with GitHub at 21:00 each day and says when this file has fallen behind.

## Bringing the apps together around My manual (10 and 11 November 2026)

Stuart asked for the apps to feed the person's manual in Regulate, with Moss keeping your place. Cairn and Picture Talk are left out. All of this is merged; none of it has been tried on a phone yet.

**Regulate** (main, phases 54 to 63; `npm run check` passes, 1,682 tests):

- #83: Talk to Moss goes back to the page you came from, and can be told that page's name on a tick. Your apps, under My manual, counts the notes each app has added.
- #84: How to raise things, in Tools.
- #85 and #86: Household agreement, in Share. Migration 0024 is applied to `regulate-preview` and the live project.
- #87: the sign-in page opens with Apple and Google; the email code is behind a small link. Passkeys are built and switched off.
- #88: "Put a step in Pace" in Talk to Moss.
- #89: the glass look (a soft glow, glass cards, a floating bar, one mint accent). Dimmed screens stay plain.

- #90 to #94 (later on 11 November): a way back from Talk to Moss while loading; Plus named in three benefits; Moss's own AI allowance; each section's own colour again; "Put a step in Pace" can start from selected words; Your apps on Today as "Get something done", opening on three jobs (deal with a letter, start something, talk it through); Talk to Moss needs its own tick before first use, with a switch in Settings; the sign-in consent names Talk to Moss and the household agreement, so every account agrees again once; Plus for testers (migration 0025, applied to both projects: `select public.grant_tester_plus('email');` in the SQL editor).

**Pace** (pace #28, merged, never compiled: the next build is the first compile): stays signed in with no signal; a hand-over arrives with its Get ready list and finish line.

**Head Untangled app** (coaching-studio #21, merged): "Add to My manual in Regulate" on My plan. Not in a build yet.

**Mull** (mull #13 and #14, merged): notes from Head Untangled are named correctly (one Swift line, never compiled: build Mull once before the next upload), and the two Moss server changes are recorded.

**Shared Moss server:** `0003` (notes from Head Untangled) and `0004` (a step from Regulate) are applied.

Waiting on Stuart:

- New builds for Regulate and Pace: `cd ~/all-projects && git pull -q && zsh scripts/testflight-all.sh regulate pace`. Then one phone check: the bar, large text, Level 1, Talk to Moss's notice, and a step sent from Moss arriving in Pace.
- Decide: the bundle price.
- Turn passkeys on: Supabase dashboard, Authentication, Passkeys, for `regulate-preview` then the live project; then `VITE_PASSKEYS_ON=true` in Netlify.
- Data protection: the assessments gain the page name sent to Moss, the household agreement (it may name people you live with) and the step sent to Pace.
- Regulate's `CLAUDE.md` still says migrations are applied by the owner; on 11 November Stuart asked Claude to apply them. The rule is his to change.

Still to do: Moss's chat inside Pace, Head Untangled and Dealt With (they still open Mull); one sign-in across Mull and Pace; Dealt With adding notes; one Plus across the apps (waits on the Paid Apps Agreement); passkeys inside the phone apps; the glass look in the other apps.

## Regulate moved to the shared server (11 November 2026, evening)

Stuart asked for the databases to be brought together, after both servers were counted and held only his own test accounts.

- **Live since 20:19:** regulate.liferegulationlab.com reads the shared Life Regulation Lab project (`xgeacgbeiivcbrgdfpbf`, Zurich). Regulate's records are in their own schema there, `regulate`; nothing of Regulate's is in `public` (regulate #95, spec section 64). Stuart signed in and saw his record.
- **Copied across** to Stuart's shared sign-in: profile and settings, levels, sleep and body logs, journal, medications and doses, cycle dates, pantry, manual. Not copied: 17 reports, AI request counts, the old hotmail test account.
- **The London project** (`bpjqmohsjddkffkqyscv`) is untouched and unused. Stuart pauses it when he is happy. Do not delete it.
- **Changed for a shared sign-in:** a person starts in Regulate through `regulate.join()`; deleting removes the Regulate record and keeps the sign-in if another app uses it; the unused-account check measures Regulate's own use; `/privacy` says Zurich and the shared sign-in. `public.lrl_still_used` on the shared server now counts a Regulate profile.
- **Set on the shared project:** Regulate's return address, its Apple bundle id and two Google client ids, passkeys for regulate.liferegulationlab.com, `regulate` among the exposed schemas, sign-ups open (`regulate.service_state.signups_open`).
- **Follow-up fixes** (regulate #96, coaching-studio #22): Cycle always listed under Record and switched on from its own tab; a whole spanner for the Tools icon; Your apps free for everyone with the apps behind "About the apps"; an Open link for Head Untangled.

Still to do:

- Phone builds: all eight apps were built and uploaded on 12 November (Regulate 0.1.0 (26), then once more after regulate #105). Still to do on a phone: existing record there, a new entry survives a restart, Apple and Google sign-in in the Regulate phone app, a step from Moss arriving in Pace with its preparation list.
- **Dashboards:** fixed in code on 12 November (dashboards #25, with regulate migration 0034): the Worker reads the shared project's `regulate` schema and shows each AI allowance on its own. It is not live until `npx wrangler deploy` is run in `worker/`; until then the card still shows the London project's stale counts.
- **Sign-in emails** on the shared project already go through MailerSend (checked 12 November 2026); nothing to change. The earlier line here, saying Supabase's built-in sender, was wrong.
- Stuart's impact assessment and transfer assessment: London becomes Zurich, and the sign-in is shared.
- `types.ts` in regulate was written by hand for the `regulate` schema; regenerate on the Mac: `npx supabase gen types typescript --project-id xgeacgbeiivcbrgdfpbf --schema regulate`.
- Netlify, lrl-regulate: the Local development value of `SUPABASE_SERVICE_ROLE_KEY` (the preview project's) is not marked secret.
- Not started: Dealt With and Whole Story onto the shared server (both are on Firebase); one sign-in screen across apps; one purchase for the collection; the Regulate sign-in standing in for the Moss link.

## Regulate: the ledger (12 November 2026)

One line for each thing built in the design review and the two code reviews. "Web" is regulate.liferegulationlab.com, which takes every merge to `main`. "Phone" is the newest TestFlight build that holds it. "Unverified" means nobody has looked at it working on a real screen; it does not mean broken. Every line passed `npm run check` and its preview build before merging; that is the only evidence unless the last column says more.

| Feature | Source | Migration | Web | Phone | Evidence | Last checked |
| --- | --- | --- | --- | --- | --- | --- |
| Google sign-in in the phone app (nonce) | #100 | none | live | built | tests; Stuart: Google and Apple work in Dealt With | 12 Nov, Regulate phone unverified |
| Settings is a list, not the set-up questions | #101 | none | live | built | tests | 12 Nov, unverified by eye |
| Review fixes: settings saved one value at a time, membership in every rule, consent fails closed, request size limit | #102 | 0027 applied | live | built | tests, SQL tests, trial on the live database | 12 Nov |
| AI allowance: a place taken before the model is called | #103, #105 | 0028, 0029 applied | live | built | tests, SQL tests | 12 Nov |
| Back to Tools from a tool; Moss settings wording | #104 | none | live | built | tests | 12 Nov, unverified by eye |
| Plan and billing always visible; Manual wording; all 200 notes counted | #106 | none | live | **not built** | tests | 12 Nov, unverified by eye |
| Tools in four groups, Help now, favourites; Food folds; light theme; opaque cards | #107 | none | live | **not built** | tests; light theme seen in screenshots | 12 Nov |
| History: 30, 90, 365 days and custom, coverage, compare, a day's entries, saved views | #108 | 0030 applied | live | **not built** | tests, SQL tests | 12 Nov, unverified by eye |
| Support cards with where each came from, recorded uses, earlier wording | #109 | 0031 applied | live | **not built** | tests, SQL tests | 12 Nov, unverified by eye |
| Shared notes say what they are about; a switch for each app's new notes | #110, mull #16, coaching-studio #23 | Moss 0006 applied | live | **not built** (Regulate and Head Untangled) | tests | 12 Nov, no note has yet travelled between two real apps |
| Recognition: a short line, optional counts, or nothing | #111 | 0032 applied | live | **not built** | tests, SQL tests | 12 Nov, unverified by eye |
| AI allowance shown on Plan and billing; LRL Collection named as not on sale yet | #112 | none | live | **not built** | tests | 12 Nov, unverified by eye |
| Plus inside the phone apps (RevenueCat), brought up to date; replaces #39 | #113 | none | live (merged 21:38 UTC) | **not built**; the first build with the new plugin | tests with stand-ins only | 12 Nov; no real purchase, no restore, no phone build |
| Recheck fixes: History counts the whole last day; a reworded card starts with its own evidence; card forms keep what was typed until saved | #114 | 0033, 0034 applied | live | **not built** | tests, SQL tests (new `card_wording.sql`) | 12 Nov, unverified by eye |
| Dashboard reads Regulate from the shared server, each AI allowance on its own | dashboards #25 | 0034 applied | **not deployed** (`npx wrangler deploy`) | no app build needed | tests; database checked (schema exposed, wrong key refused) | 12 Nov, no live reading seen |

**Not migrated:** the 17 generated reports on the London project were not copied to the shared server on 11 November. They are still on London (`bpjqmohsjddkffkqyscv`, untouched). AI request counts were not copied either.

**From the recheck of 12 November, not done:** selected support cards in the shared guide and reports; the landing page showing the Manual and History; the platform list (Android cycle import is not built); the 17 London reports archived or reconciled; Head Untangled, Pace, Mull, Dealt With and Whole Story contributions beyond what is in the table; "I support someone" in Your apps. Native purchase, restore and Collection access are unproven until the stores are set up.

**Asked for in the design review and not built:** milestones and a collection (recognition); the wider two-column layout on a wide screen; a sleep bar chart and cycle markers in History; saved versions of the whole Manual; "Sign out everywhere"; Pace sending task outcomes, Mull sending approved insights and Dealt With sending context to the Manual; LRL Collection as something that can be bought (it is named on Plan and billing as not on sale yet).

**Buying inside the phone apps** is in the code (regulate #113) and switched off. Before anything can be bought: the two products in App Store Connect and Google Play, the RevenueCat project with its `plus` entitlement, the two public RevenueCat keys in `.env.shell`, `REVENUECAT_SECRET_KEY` and `REVENUECAT_WEBHOOK_SECRET` in Netlify, the webhook address, and `VITE_PLUS_ON_SALE` true (regulate `docs/DEPLOY.md`). If the next Regulate phone build fails on the RevenueCat package, that is #113.

**Needs a person:** one Regulate phone build and one Head Untangled build, then a pass on the phone; `types.ts` regenerated on the Mac (it has been edited by hand since 0026).

## The letter, Pace and back (11 November 2026, late)

- **A fault found and put right on the shared server.** Until tonight no app could send a step to Pace or save a Moss note: the server refused every one (the rule counted its own table). Both tables were empty. Fixed in Moss server 0005 (mull #15, applied and tested).
- **Dealt With** (life-admin #21, merged): a step put into Pace now says sent, added to Pace, finished in Pace or done here, as separate things. Sending again never makes two tasks. `dealtwith://item/<id>` opens the letter in the phone app.
- **Pace** (pace #29, open): tells the server when a task from another app is finished or un-ticked, and has "Open in Dealt With". Written without a Swift compiler: merge only after the Build check on the Mac passes.
- **Regulate** #99 merged (Moss: where a long talk is sent from, Start again asks first).
- Dealt With's Moss link is still the older one (the email of a Mull or Pace account). Now that Dealt With uses the shared sign-in it could use that instead; not done.

## Waiting on Stuart (business)

- App Store Connect, Business page: the **W-9** tax form and the **Paid Apps Agreement** are outstanding. Paid Apps is needed before any subscription or paid app (Mull, Regulate Plus) can go on sale.
- Desk is a personal app (Stuart, 25 Oct): it stays in TestFlight for Stuart only, never goes on sale or on any website.

## Before any app goes to App Store review or Google Play

- Check every app offers **Sign in with Apple** and **Sign in with Google** where it has an account. Not all do yet (Stuart, 25 October 2026). Apple requires Sign in with Apple when an app offers another sign-in such as Google. Check each app's sign-in screen on a phone before it is submitted.

## Apps on App Store Connect

All under team PCA5FZ26HM. "Testers" is the external group (Apple reviews each new version's first build); "Internal" or "Me" is Stuart's own group (no review).

| App | Newest build | TestFlight | Repo and branch | Open PRs |
| --- | --- | --- | --- | --- |
| Pace | 0.2 (10), Talk to Moss (opens Mull), after 0.2 (9) with Moss in the middle of Today, uploaded late on 25 Oct (0.2 (8) earlier the same evening) | Approved. 0.1 (1), 0.2 (5) and 0.2 (6) Testing in Testers. 0.2 (8) and (9) internal only (Stuart, 25 Oct). | pace, main | #2 Share with Coach |
| Mull | 1.0 (6), Sign in with Apple and Google (mull #8) and Moss on the home page, uploaded late on 25 Oct | Approved. 1.0 (3) Testing in Testers; 1.0 (5) and (6) internal only (Stuart, 25 Oct). Review sign-in: review@liferegulationlab.com. | mull, claude/project-thread-ni92pc (the repo's default; there is no main yet) | none |
| Desk | iOS and macOS 1.0.0 (2); iOS 1.0.0 (3) with the icon fix | Approved. iOS 1.0.0 (2), iOS 1.0.0 (3) and macOS 1.0.0 (2) all Testing in Testers. | Desk, main | none |
| Regulate | 0.1.0 (9), Talk to Moss (Regulate's own coaching chat, regulate #66 and #67; needs migration 0019 on the live project), after 0.1.0 (8) with Moss in the middle of Me with the fix for the "This page didn't load" error in 0.1.0 (7) (regulate #65), uploaded late on 25 Oct | Internal only ("Me" group). Not for outside testers. | regulate, main | #37 Coming soon; #38 and #39 drafts (phone sign-in, RevenueCat); #40 transfers wording |
| Cairn | 1.0 (3), the teal accent, uploaded 25 Oct 21:43 | 1.0 (1) submitted 23 Oct to the external "Testers" group. 1.0 (3) internal only (Stuart, 25 Oct). | cairn, main | #1 DPIA pack |
| Head Untangled app | 1.0 (7), Talk to Moss (opens Mull), after 1.0 (6) with the new Moss, uploaded late on 25 Oct | Approved. 1.0 (3) Testing in "Testers"; 1.0 (5) internal only (Stuart, 25 Oct). Also in internal "Test". | coaching-studio, main | #5 Resets |

Uploads: `scripts/testflight-all.sh` builds and uploads all five apps above (not Desk, not Picture Talk) from the newest GitHub code, in one Terminal command on the Mac (25 Oct).

Merged today: Pace #5 and #6, Mull #1, Desk #7, #8 and #9, Regulate #53 and #54, Cairn #8 (iPhone and iPad app, Delete my account), liferegulationlab-site #9, #10, #11 and #12, all-projects #3, #4 and #5 (the evening sync check).

### Next steps

1. **Cairn:** wait for Beta App Review of 1.0 (1). If Apple asks for a demo login, finish the review@liferegulationlab.com account in Willow House and add it to the Test Information. Next upload must be build 4 or higher.
2. **Pace:** try the watch app on a real watch. Check the 0.2 (6) What to Test text (written as a guess). Next upload must be build 11 or higher.
3. **Mull:** try the watch app and the new Apple and Google sign-in. Subscriptions still need the Paid Apps Agreement. Next upload must be build 7 or higher.
4. **Desk:** nothing waiting.
5. **Regulate:** 0.1.0 (9) uploaded 25 Oct; next upload must be build 10 or higher. Stays closed to new accounts. Open privacy and data protection actions are in the Regulate status note (Claude project files/Regulate/Regulate-Status.md).
6. **Head Untangled app:** testers have 1.0 (3); 1.0 (7) uploaded 25 Oct. Next upload must be build 8 or higher. Decide on PR #5 (Resets).

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
| Dashboards | dashboards, main | 10 November (PR #24, merged; Worker deployed): app health is live. The Dashboard app's Apps card has an entry for Regulate, Cairn, Mull, Pace, the Head Untangled app, Picture Talk and Desk, from counts read out of each app's database, and all seven are answering. Each of the three databases has a counts-only function, `dashboard_health`, that answers only to its own secret (kept in `Desktop/Private - not in cloud/`). A database not answering on two checks in a row sends a push. Regulate's side (regulate #81, and its `types.ts` in #82) merged 10 November. Still open: cairn #11 (run `pnpm db:test` with Docker, then merge). Both functions are already applied to the live databases. |
| Coach (private) | Claude project files/private-coach, not in git | Stuart's own app. Mull is the App Store version. |
| Ledger | ledger, main | 26 October: Ledger 2 (PR #1): LLC and personal books, double entry, reconciled balances, iPhone receipts through iCloud Drive, encrypted backups each evening, and a tax centre for the US, Guernsey and the UK. Private, on the Mac only. |

## Replaced Shorts and videos

| Date | Replaced | Removed |
| --- | --- | --- |
| 30 Oct 2026 | Head Untangled Shorts S49–S56: Stuart approved new openings (the key fact first) at 06:31 | The old cuts are gone from `lrl-media/from-cloud/Head-Untangled/shorts/s48-s57-2026-10-29/` (replaced in place) and from project files. All 32 Metricool bookings (TikTok, YouTube, Pinterest, Facebook, 31 Oct–3 Nov) now use the new files, each checked against the approved file. The old cuts were never posted. They stay in Metricool's media library, because the connector can't delete from it. |
| 31 Oct 2026 | Head Untangled Shorts S62–S73, S75, S76 and S79: Stuart approved the re-voiced versions (Alex names the free printable in the last line; S68 with the medication line moved mid-sentence, S73 with the headphones fixed) at 19:51 | The old cuts are gone from project files (`head-untangled-shorts-s62-s64`, `-s62-s63-natural-adhd`, `-s65-s74`, `-s75`, `-s76-s79`) and from `lrl-media/from-cloud/Head-Untangled/shorts/` (the `s62-s64`, `s62-s63-natural-adhd`, `s65-s74`, `s75` and `s76-s79` date folders). The approved files are in project files `head-untangled-shorts-s62-s79-printable-line` and `lrl-media/from-cloud/Head-Untangled/shorts/s62-s79-printable-line-2026-10-31/`. All 75 Metricool bookings (YouTube, Facebook, Pinterest, TikTok, Instagram; 8 Nov–11 Dec) now use the new files. The old cuts were never posted. They stay in Metricool's media library, because the connector can't delete from it. S74 (no printable) is unchanged. S77 and S78 were approved at 20:29 and swapped the same way (old cuts removed from project files `head-untangled-shorts-s76-s79` and the `s76-s79` cloud folder). |

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
