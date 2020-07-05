# Komplete Kontrol DAW Integration for FL Studio
Implementation of the deep integration mode found on Native Instruments' Komplete Kontrol keyboards for FL Studio.

This script aims to support all the features of this mode, offering the same features found on supported DAWs like Ableton Live or Logic Pro X.

For installation know-how and info on how to use the script, go to the wiki of the repository.

## Main features
 - Takes advantage of the DAW integration mode
 - Playback control right from the device
 - Full mixer support, including peak meters on S-Series MK2 devices

## Compatible devices
### Komplete Kontrol
 - [x] Komplete Kontrol A25/49/61
 - [x] Komplete Kontrol M32 (works the same way A-Series do)
 - [x] Komplete Kontrol S49/61/88 MK2
 - [ ] Komplete Kontrol S49/49/61/88 MK1 (supposed to work as A-Series, not tested)
### Maschine
As of today, this script hasn't been tested on Maschine devices. However, some might work due to their similarities in functionality with Komplete Kontrol keyboards.
 - [ ] Maschine MK3 (supposed to work as S-Series MK2, but not tested yet)
 - [ ] Maschine Studio (supposed to work as S-Series MK2, but not tested yet)
 - [ ] Maschine MK2
 - [ ] Maschine MK1
 - [ ] Maschine Mikro MK3 (supposed to work as A-Series, not tested)
 - [ ] Maschine Mikro MK2
 - [ ] Maschine Mikro MK1

## Known issues
 - **Performance issues:** In certain situations, actions coming from the device into FL Studio might get up to 5 seconds to have an effect on FL Studio. However, it doesn't affect performance of the software in any way neither on note input (MIDI and DAW Control instructions are sent by different MIDI devices). The delay is only for input processing coming from the button panel at the top of the device and a fix is being developed for this.
 - **Automatic Komplete Kontrol instance switching:** It is already implemented in the compatibility layer, but the info that is needed from FL Studio to do so can't be gotten with the current API scope. Waiting for Image-Line to add plugin parameter read/write capabilities to the API for this.
 - **Manual Komplete Kontrol instance switching:** In S-Series devices, DAW integration seems to disable the option to switch instances manually using the keyboard, relying on the host DAW to tell the device which instance to control. Due to the automatic instance switching not being compatible with FL Studio at the moment, it might be that the only way to change instances for S-Series users once the DAW integration has ben initiated is to do it manually with a mouse.