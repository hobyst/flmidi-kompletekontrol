# Komplete Kontrol DAW Integration for FL Studio
Implementation of the deep integration mode found on Native Instruments' Komplete Kontrol keyboards for FL Studio.

This script aims to support all the features of this mode, offering the same features found on supported DAWs like Ableton Live or Logic Pro X.

## Installing the script

On Windows
```bat
cd "%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware"

REM Download the latest stable release
git clone https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"

REM Download the latest beta version (might have bugs)
git clone -b beta https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"

REM Download the latest alpha version (it will have bugs for sure)
git clone -b dev https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"
```
On macOS
```bash
cd "Documents/Image-Line/FL Studio/Settings/Hardware/"

# Download the latest stable release
git clone https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"

# Download the latest beta version (might have bugs)
git clone -b beta https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"

# Download the latest alpha version (it will have bugs for sure)
git clone -b dev https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"
```

## Updating the script

On Windows
```bat
cd "%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware"

REM Removes the old version of the script
rmdir /Q /S "Native Instruments Komplete Kontrol"

REM Download the latest stable release
git clone https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"

REM Download the latest beta version (might have bugs)
git clone -b beta https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"

REM Download the latest alpha version (it will have bugs for sure)
git clone -b dev https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"
```

On macOS
```bash
cd "Documents/Image-Line/FL Studio/Settings/Hardware/"

# Removes the old version of the script
rm -r "Native Instruments Komplete Kontrol"

# Download the latest stable release
git clone https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"

# Download the latest beta version (might have bugs)
git clone -b beta https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"

# Download the latest alpha version (it will have bugs for sure)
git clone -b dev https://github.com/hobyst/flmidi-kompletekontrol.git --recurse-submodules "Native Instruments Komplete Kontrol"
```