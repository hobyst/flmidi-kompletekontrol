# Komplete Kontrol DAW Integration for FL Studio

Implementation of the deep integration mode found on Native Instruments' Komplete Kontrol keyboards for FL Studio.

This script aims to support all the features of this mode, offering the same features found on supported DAWs like Ableton Live or Logic Pro X.

For installation know-how and info on how to use the script, go to the [wiki](https://github.com/hobyst/flmidi-kompletekontrol/wiki) of the repository.

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

- [ ] ~~Maschine Mikro MK3~~ (doesn't have DAW integration mode)

- [ ] Maschine Mikro MK2

- [ ] Maschine Mikro MK1

## Known issues

- [**Performance issues on FL Studio 20.7.2 and up (Windows):**](https://github.com/hobyst/flmidi-kompletekontrol/issues/8) On FL Studio 20.7.2 and upwards, a bug was discovered that makes the script not to work sometimes and causes a performance drawback due to the constant error printing on the Script output. The only workaround for this is to reload the script if you notice any kind of performance issue. Go to `View > Script output > "the tab with the DAW device name on it"` and click on the `Reload script` button until the cascade stops and no errors seem to happen.

- [**Automatic Komplete Kontrol instance switching:**](https://github.com/hobyst/flmidi-kompletekontrol/issues/3) It is already implemented in the compatibility layer, but the info that is needed from FL Studio to do so can't be gotten with the current API scope. Waiting for Image-Line to add plugin parameter read/write capabilities to the API for this.

- [**Manual Komplete Kontrol instance switching:**](https://github.com/hobyst/flmidi-kompletekontrol/issues/4) In S-Series devices, DAW integration seems to disable the option to switch instances manually using the keyboard, relying on the host DAW to tell the device which instance to control. Due to the automatic instance switching not being compatible with FL Studio at the moment, it might be that the only way to change instances for S-Series users once the DAW integration has ben initiated is to do it manually with a mouse.

- [**QUANTIZE and AUTO buttons don't work as expected:**](https://github.com/hobyst/flmidi-kompletekontrol/issues/5) Quantize and toggling automation recording on/off isn't supported yet on the actual MIDI API scope. There's a workaround to get to the quantize buttons by getting into the menus and emulating key pressings but it's slow and buggy. Instead, they switch between windows (browser isn't included on this) and trigger full-screen plugin browser respectively.

## Special thanks

- [Duwayne Wright](https://github.com/soundwrightpro): Coding help

- [B3NYBOI](https://www.youtube.com/channel/UC8C58LOA00jy600kt6h1hTw/): Early testing

- [Tunz Amazin](https://twitter.com/HearMyTunz): Early testing

- [Juanpe](https://www.youtube.com/channel/UC_3ONcvDjAyr1POm2ieefPg/): Early testing

- [Jürgen Moßgraber](https://github.com/git-moss): Implementation reference