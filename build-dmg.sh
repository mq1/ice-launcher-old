#!/bin/sh

ref_name="$1"
arch="$(uname -m)"

test -f "IceLauncher-${ref_name}-macos-${arch}.dmg" && rm "IceLauncher-${ref_name}-macos-${arch}.dmg"

create-dmg \
    --volname "Ice Launcher Installer" \
    --icon-size 100 \
    --icon "Ice Launcher.app" 0 100 \
    --hide-extension "Ice Launcher.app" \
    --app-drop-link 200 100 \
    --no-internet-enable \
    --format ULMO \
    "IceLauncher-${ref_name}-macos-${arch}.dmg" \
    dist/Ice\ Launcher.app
