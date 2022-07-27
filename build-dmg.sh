#!/bin/sh

arch="$(uname -m)"

test -f "IceLauncher-macos-${arch}.dmg" && rm "IceLauncher-macos-${arch}.dmg"

create-dmg \
    --volname "Ice Launcher Installer" \
    --icon-size 100 \
    --icon "Ice Launcher.app" 0 100 \
    --hide-extension "Ice Launcher.app" \
    --app-drop-link 200 100 \
    --no-internet-enable \
    --format ULMO \
    "IceLauncher-macos-${arch}.dmg" \
    dist/Ice\ Launcher.app
