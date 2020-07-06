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

- [x] Komplete Kontrol M32 (works the same way A-Series does)

- [x] Komplete Kontrol S49/61/88 MK2

- [ ] Komplete Kontrol S25/49/61/88 MK1 (supposed to work as A-Series, not tested)

### Maschine

As of today, this script hasn't been tested on Maschine devices. However, some might work due to their similarities in functionality with Komplete Kontrol keyboards.

- [ ] Maschine MK3 (supposed to work as S-Series MK2, not tested)

- [ ] Maschine Studio (supposed to work as S-Series MK2, not tested)

- [ ] Maschine MK2

- [ ] Maschine MK1

- [ ] Maschine Mikro MK3 (supposed to work as A-Series, not tested)

- [ ] Maschine Mikro MK2

- [ ] Maschine Mikro MK1

## Known issues

- 

- **4D Encoder's built-in D-pad axis might be inverted:** A-Series and S-Series have their encoder axis inverted and by default, the script maps encoder events as if you were using a S-Series device. You can solve this by opening going to the script folder and inside the `device_Komplete Kontrol.py` set `DEVICE_SERIES` to the kind of the device you are using. If you have more than one NI device and don't want to make multiple files for that, you can set it on runtime by going to View > Script output, selecting the name of the MIDI device that isn't acting as expected and run the following line:
  
  ```python
   DEVICE_SERIES = "<series of your device>"
  ```

- **Automatic Komplete Kontrol instance switching:** It is already implemented in the compatibility layer, but the info that is needed from FL Studio to do so can't be gotten with the current API scope. Waiting for Image-Line to add plugin parameter read/write capabilities to the API for this.

- **Manual Komplete Kontrol instance switching:** In S-Series devices, DAW integration seems to disable the option to switch instances manually using the keyboard, relying on the host DAW to tell the device which instance to control. Due to the automatic instance switching not being compatible with FL Studio at the moment, it might be that the only way to change instances for S-Series users once the DAW integration has ben initiated is to do it manually with a mouse.

- **QUANTIZE and AUTO buttons don't work as expected:** Quantize and toggling automation recording on/off isn't supported yet on the actual MIDI API scope. There's a workaround to get to the quantize buttons by getting into the menus and emulating key pressings but it's slow and buggy. Instead, they switch between windows (browser isn't included on this) and trigger full-screen plugin browser respectively.

## Special thanks

- [Duwayne Wright](https://github.com/soundwrightpro): Coding help

- [B3NYBOI](https://www.youtube.com/channel/UC8C58LOA00jy600kt6h1hTw/): Early testing

- [Tunz Amazin](https://twitter.com/HearMyTunz): Early testing

- Juanpe: Early testing

- [Jürgen Moßgraber](https://github.com/git-moss): Implementation reference