# Mac builds on Stuart's Mac (self-hosted runners)

Set up 25 Oct 2026. GitHub Actions has 3,000 free minutes a month, and GitHub's Macs count ten times.
So the macOS and iOS jobs run on Stuart's own Mac instead, for free.

## What is installed

- One runner per repo, because LifeRegulationLab is a personal account (organisations can share one
  runner, personal accounts can't): `pace`, `mull`, `Desk`, `picture-talk`.
- Runner names `stuarts-mac-<repo>`, labels `self-hosted, macOS, ARM64, xcode`, runner 2.338.1.
- Folders: `~/actions-runners/<repo>` on the Mac (not on the Desktop, so not copied to the cloud).
- Each starts at login as a LaunchAgent: `~/Library/LaunchAgents/actions.runner.LifeRegulationLab-<repo>.stuarts-mac-<repo>.plist`.
- Each runner's `.env` sets `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`, so jobs use full Xcode
  without changing the Mac's own default (no sudo).

## How workflows use it

```yaml
on:
  workflow_dispatch:
    inputs:
      runner:
        type: choice
        options: [mac, github]
        default: mac
jobs:
  build:
    runs-on: ${{ inputs.runner == 'github' && 'macos-latest' || fromJSON('["self-hosted", "macOS"]') }}
```

- Pull request runs and hand runs go to the Mac by default.
- While the Mac is off, jobs wait in the queue. They never move to GitHub's paid Macs by themselves.
  GitHub cancels a job that has waited 24 hours; start it again when the Mac is on.
- Fallback: run the workflow by hand from the Actions tab and pick `github`. That uses paid minutes.
- Done in pace (#16), mull (#6) and Desk (#12). Picture Talk is switching its own checks.

## Safety

A runner lets GitHub run code from the repo on the Mac. That is safe because these repos are private, so
only Stuart's own pushes run there. Never add a self-hosted runner to a public repo (all-projects, whole-story,
life-admin and nd-vault are public), and never make a repo with a runner public.

## Looking after it

- Status: `cd ~/actions-runners/<repo> && ./svc.sh status`. Stop or start: `./svc.sh stop` / `./svc.sh start`.
- Remove one: `./svc.sh uninstall`, then `./config.sh remove --token <removal token>`
  (`gh api -X POST repos/LifeRegulationLab/<repo>/actions/runners/remove-token --jq .token`).
- Add a repo: copy the steps above with a registration token from
  `gh api -X POST repos/LifeRegulationLab/<repo>/actions/runners/registration-token --jq .token`.
- The runner updates itself.
