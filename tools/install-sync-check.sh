#!/bin/zsh
# Sets the sync check to run every evening at 21:00 on this Mac.
# Run once:   zsh ~/all-projects/tools/install-sync-check.sh
# To stop it: zsh ~/all-projects/tools/install-sync-check.sh --remove
# Author: Stuart Houlihan

LABEL="com.liferegulationlab.sync-check"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
SCRIPT="$(cd "$(dirname "$0")" && pwd)/sync-check.py"
LOG="$HOME/Library/Logs/sync-check.log"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null

if [[ "$1" == "--remove" ]]; then
  [[ -f "$PLIST" ]] && mkdir -p "$HOME/Desktop/_to_delete" && mv "$PLIST" "$HOME/Desktop/_to_delete/"
  echo "Sync check stopped. The schedule file is in Desktop/_to_delete."
  exit 0
fi

mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$SCRIPT</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>21</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
EOF

launchctl bootstrap "gui/$(id -u)" "$PLIST" && echo "Sync check set for 21:00 each evening. Log: $LOG"
