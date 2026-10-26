#!/bin/zsh
# Builds every iPhone app that is in App Store Connect from its newest GitHub code and uploads it to
# TestFlight. Runs on Stuart's Mac, in Terminal (not through a GitHub runner: a runner runs in the
# background, where the keychain is locked and signing fails):
#
#   cd ~/all-projects && git pull -q && zsh scripts/testflight-all.sh
#
# Or only some apps:  zsh scripts/testflight-all.sh pace mull
# Apps: pace, mull, regulate, headuntangled, cairn, wholestory, dealtwith. Not Desk (personal) and not Picture Talk (own script).
#
# Each app is built in a clean copy under ~/testflight-builds (outside the Desktop, so not copied to
# the cloud), so the Desktop folders are never changed. Build numbers are given on the command line;
# if App Store Connect already has that number, the next one up is tried (up to three times).
# The result of each app is written to the summary in
# Desktop/Claude project files/Life Regulation Lab/testflight/, and STATUS.md is updated from it.
# Needs: Xcode signed in to team PCA5FZ26HM, gh signed in, Node 22. If macOS asks about codesign
# and the keychain, type the Mac password and click Always Allow.
set -uo pipefail

TEAM=PCA5FZ26HM
OWNER=LifeRegulationLab
WORK=~/testflight-builds
NOTES=~/"Desktop/Claude project files/Life Regulation Lab/testflight"
STAMP=$(date +%Y-%m-%d-%H%M)
SUMMARY=$NOTES/summary-$STAMP.txt
export DEVELOPER_DIR=${DEVELOPER_DIR:-/Applications/Xcode.app/Contents/Developer}
mkdir -p $WORK/logs "$NOTES"

# app  repo  branch  first build number to try
APPS=(
  "pace            pace             main                          12"
  "mull            mull             claude/project-thread-ni92pc  8"
  "regulate        regulate         main                          11"
  "headuntangled   coaching-studio  main                          9"
  "cairn           cairn            main                          4"
  "wholestory      whole-story      main                          7"
  "dealtwith       life-admin       main                          3"
)
if (( $# )); then WANT=($@); else WANT=(pace mull regulate headuntangled cairn wholestory dealtwith); fi

EXPORT=$WORK/ExportOptions.plist
cat > $EXPORT <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>method</key><string>app-store-connect</string>
	<key>destination</key><string>upload</string>
	<key>teamID</key><string>$TEAM</string>
	<key>signingStyle</key><string>automatic</string>
	<key>manageAppVersionAndBuildNumber</key><false/>
</dict>
</plist>
EOF

say() { print -r -- "$*" | tee -a "$SUMMARY"; }

# A clean copy of the repo's newest code on the branch, in $WORK/<repo>.
fetch() {
  local repo=$1 branch=$2 dir=$WORK/$1
  if [[ -d $dir/.git ]]; then
    git -C $dir fetch -q origin $branch && git -C $dir checkout -q --force --detach FETCH_HEAD && git -C $dir clean -fdq
  else
    gh repo clone $OWNER/$repo $dir -- -q --branch $branch
  fi
}

# Archive and upload; on a build number App Store Connect already has, try the next one.

upload() {
  local name=$1 project=$2 scheme=$3 build=$4 log=$WORK/logs/$1.log tries=0
  : > $log
  while (( tries < 6 )); do
    local archive=$WORK/archives/$name-$build.xcarchive
    rm -rf $archive $WORK/export/$name
    print "  archiving $name ($build)…"
    if ! xcodebuild -project $project -scheme $scheme -configuration Release -destination 'generic/platform=iOS' \
        -archivePath $archive -allowProvisioningUpdates DEVELOPMENT_TEAM=$TEAM CURRENT_PROJECT_VERSION=$build \
        archive >> $log 2>&1; then
      return 1
    fi
    print "  uploading $name ($build)…"
    if xcodebuild -exportArchive -archivePath $archive -exportOptionsPlist $EXPORT \
        -exportPath $WORK/export/$name -allowProvisioningUpdates >> $log 2>&1; then
      BUILT=$build
      return 0
    fi
    if tail -40 $log | grep -qiE 'bundle version|previously uploaded|DUPLICATE|already been used|already exists'; then
      build=$((build + 1)); tries=$((tries + 1))
    else
      return 1
    fi
  done
  return 1
}

# A Capacitor app on its own Firebase project (Whole Story, Dealt With). Firebase's Google file is not
# in the repo: kept once in $WORK, made by the Firebase CLI if missing (registering the iPhone app in
# the project the first time).
firebase_app() {
  local app=$1 dir=$2 project=$3 bundle=$4 build=$5 gfile=$WORK/GoogleService-Info-$1.plist
  local findid="let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const a=(JSON.parse(s).result||[]).find(x=>x.namespace==='$bundle');process.stdout.write(a?a.appId:'')})"
  if [[ ! -s $gfile ]]; then
    local fid=$(npx -y firebase-tools apps:list IOS --project $project --json 2>/dev/null | node -e "$findid")
    if [[ -z $fid ]]; then
      npx -y firebase-tools apps:create IOS "$app iPhone" --bundle-id $bundle --project $project >> $WORK/logs/$app.log 2>&1
      fid=$(npx -y firebase-tools apps:list IOS --project $project --json 2>/dev/null | node -e "$findid")
    fi
    [[ -n $fid ]] && npx -y firebase-tools apps:sdkconfig IOS "$fid" --project $project -o $gfile >> $WORK/logs/$app.log 2>&1
  fi
  local reversed=$(/usr/libexec/PlistBuddy -c 'Print :REVERSED_CLIENT_ID' $gfile 2>/dev/null || true)
  if [[ -z $reversed ]]; then
    print "  no REVERSED_CLIENT_ID in $gfile: switch on Google sign-in in Firebase ($project), delete the file and run again" >> $WORK/logs/$app.log
    return 1
  fi
  cd $dir && npm ci --no-audit --no-fund >> $WORK/logs/$app.log 2>&1 \
    && npx vite build >> $WORK/logs/$app.log 2>&1 \
    && npx cap sync ios >> $WORK/logs/$app.log 2>&1 \
    && cp $gfile ios/App/App/GoogleService-Info.plist \
    && sed -i '' "s/GOOGLE_REVERSED_CLIENT_ID/$reversed/" ios/App/App/Info.plist \
    && cd ios/App && upload $app App.xcodeproj App $build
}

build_app() {
  local app=$1 repo=$2 branch=$3 build=$4 dir=$WORK/$2
  print "\n== $app"
  fetch $repo $branch >> $WORK/logs/$app.log 2>&1 || { say "$app: NOT UPLOADED (could not get the code from GitHub)"; return; }
  local commit=$(git -C $dir log -1 --format='%h %s' | cut -c1-90)
  case $app in
    pace)
      (cd $dir && upload pace Pace.xcodeproj PaceMobile $build) ;;
    mull)
      (cd $dir && upload mull Coach.xcodeproj Coach $build) ;;
    regulate)
      (cd $dir && npm ci --no-audit --no-fund >> $WORK/logs/$app.log 2>&1 \
        && npx vite build --mode shell >> $WORK/logs/$app.log 2>&1 \
        && npx cap sync ios >> $WORK/logs/$app.log 2>&1 \
        && cd ios/App && upload regulate App.xcodeproj App $build) ;;
    headuntangled)
      (cd $dir && npm ci --no-audit --no-fund >> $WORK/logs/$app.log 2>&1 \
        && npx vite build >> $WORK/logs/$app.log 2>&1 \
        && npx cap sync ios >> $WORK/logs/$app.log 2>&1 \
        && cd ios/App && upload headuntangled App.xcodeproj App $build) ;;
    cairn)
      # The app's public Supabase address and anon key are the live site's own (shipped to every
      # browser); read them from app.cairncare.app so they are never written into a repo.
      local js=$(curl -fsSL https://app.cairncare.app/ | grep -o '/assets/[^"]*\.js' | sort -u | while read -r p; do curl -fsSL "https://app.cairncare.app$p"; done)
      local url=$(print -r -- $js | grep -o 'https://[a-z0-9]*\.supabase\.co' | head -1)
      local key=$(print -r -- $js | grep -oE 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+' | head -1)
      if [[ -z $url || -z $key ]]; then say "$app: NOT UPLOADED (could not read the live site's Supabase address)"; return; fi
      local pnpm=(corepack pnpm); command -v corepack >/dev/null || pnpm=(npx -y pnpm@12.8.1)
      (cd $dir && $pnpm install --frozen-lockfile >> $WORK/logs/$app.log 2>&1 \
        && VITE_SUPABASE_URL=$url VITE_SUPABASE_ANON_KEY=$key VITE_AI_ENABLED=false \
           $pnpm --filter @cairn/web build:app >> $WORK/logs/$app.log 2>&1 \
        && cd apps/web/ios/App && upload cairn App.xcodeproj App $build) ;;
    wholestory)
      (firebase_app $app $dir whole-story-lrl com.liferegulationlab.wholestory $build) ;;
    dealtwith)
      (firebase_app $app $dir dealt-with-lrl com.liferegulationlab.dealtwith $build) ;;
  esac
  local result=$?
  # The upload ran in a subshell, so read the number from the newest archive it made.
  BUILT=$(ls -t $WORK/archives 2>/dev/null | grep "^$app-" | head -1 | sed -E "s/^$app-([0-9]+)\.xcarchive$/\1/")
  if (( result == 0 )); then
    say "$app: UPLOADED build $BUILT from $repo $branch ($commit)"
  else
    say "$app: NOT UPLOADED. Last lines of the log ($WORK/logs/$app.log):"
    grep -E 'error|Error|failed|FAILED' $WORK/logs/$app.log | tail -6 | sed 's/^/    /' | tee -a "$SUMMARY"
  fi
}

say "TestFlight uploads, $(date '+%d %b %Y %H:%M') on $(scutil --get ComputerName 2>/dev/null)"
for line in $APPS; do
  parts=(${=line})
  (( ${WANT[(Ie)${parts[1]}]} )) && build_app $parts
done
say "\nApple takes 10 to 30 minutes to process each build before it shows in TestFlight."
print "\nSummary saved in Claude project files, Life Regulation Lab, testflight."
