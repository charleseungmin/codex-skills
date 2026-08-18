---
name: adb-device-control
description: Use when controlling an Android device through adb, including launching apps, tapping/swiping, capturing screenshots, saving logcat evidence, setting adb reverse, checking the current Activity, or doing hands-on app navigation/testing on a connected device.
metadata:
  short-description: Control Android devices via adb with screenshots and logs
---

# ADB Device Control

Use this skill whenever the user asks to operate a connected Android device, verify a screen on-device, navigate through an app, run adb commands, capture screenshots, inspect logcat, or set up local-server testing through `adb reverse`.

## Default Workflow

1. Confirm a device is connected:
   ```powershell
   C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 status
   ```
2. Start a recorded session before manual navigation:
   ```powershell
   C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 start -Label exofit-home
   ```
3. Use scripted actions so every step saves evidence:
   ```powershell
   C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 launch -Package com.exosystems.fit
   C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 tap -X 720 -Y 205
   C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 swipe -X1 700 -Y1 1900 -X2 700 -Y2 700 -Duration 350
   C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 text -Text "hello"
   ```
4. Capture current state after any non-scripted action:
   ```powershell
   C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 capture -Name after_manual_step
   ```
5. For local server testing, set reverse explicitly:
   ```powershell
   C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 reverse -Port 18089
   ```

## Evidence Policy

Prefer the script commands over raw `adb input` because each action stores:

- screenshot PNG
- recent logcat text
- current foreground Activity
- executed action metadata in `actions.jsonl`

Artifacts are stored under:

```text
<repo>\artifacts\adb\<timestamp-label>\
```

If the repo path is unclear, pass `-OutRoot <path>`.

## Launching Apps

Use `launch -Package ...` first. It uses Android monkey launcher intent, which works even when internal Activities are `exported=false`.

If the user asks to open a non-exported Activity directly, try normal `am start` only if appropriate, but expect `SecurityException`. Fall back to the launcher/Splash route and navigate with taps.

## Reading Screens

First try screenshots. `uiautomator dump` may crash on some devices, so do not rely on it as the only verification path. Use:

```powershell
C:\Users\lenovo\.codex\skills\adb-device-control\scripts\adb-device.ps1 screenshot -Name current
```
Then inspect the saved image with the image viewer tool.

## Common Packages

For exoFit, check installed packages first:

```powershell
adb shell pm list packages | Select-String exosystems
```

Common candidates:

- `com.exosystems.fit`
- `com.exosystems.fit.test`
