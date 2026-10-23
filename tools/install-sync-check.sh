#!/bin/zsh
# Sets the sync check to run every evening at 21:00 on this Mac.
# Run once:   zsh ~/all-projects/tools/install-sync-check.sh
# To stop it: zsh ~/all-projects/tools/install-sync-check.sh --remove
#
# The check runs inside a small app, "Sync Check", in ~/Applications. macOS then asks
# once, with an Allow button, before the app reads the Desktop, iCloud Drive and
# Google Drive, so nothing needs adding to Full Disk Access by hand.
# Author: Stuart Houlihan

LABEL="com.liferegulationlab.sync-check"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
SCRIPT="$(cd "$(dirname "$0")" && pwd)/sync-check.py"
APP="$HOME/Applications/Sync Check.app"
LOG="$HOME/Library/Logs/sync-check.log"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null

if [[ "$1" == "--remove" ]]; then
  mkdir -p "$HOME/Desktop/_to_delete"
  [[ -f "$PLIST" ]] && mv "$PLIST" "$HOME/Desktop/_to_delete/"
  [[ -d "$APP" ]] && mv "$APP" "$HOME/Desktop/_to_delete/"
  echo "Sync check stopped. Its files are in Desktop/_to_delete."
  exit 0
fi

# The app: runs the check and writes to the log.
mkdir -p "$HOME/Applications"
[[ -d "$APP" ]] && mkdir -p "$HOME/Desktop/_to_delete" && mv "$APP" "$HOME/Desktop/_to_delete/Sync Check $(date +%Y%m%d-%H%M%S).app"
osacompile -o "$APP" -e "do shell script \"/usr/bin/python3 '$SCRIPT' >> '$LOG' 2>&1\""
/usr/libexec/PlistBuddy -c "Add :LSUIElement bool true" "$APP/Contents/Info.plist" 2>/dev/null
codesign --force --sign - "$APP" 2>/dev/null

mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/open</string>
    <string>-g</string>
    <string>$APP</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>21</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
</dict>
</plist>
EOF

launchctl bootstrap "gui/$(id -u)" "$PLIST" && echo "Sync check set for 21:00 each evening. Log: $LOG"

# First run now, so the Allow questions appear while you are at the Mac.
open "$APP"
echo "Running the first check now. If macOS asks whether Sync Check may open files, press Allow each time."
