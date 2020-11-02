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

- [**QUANTIZE and AUTO buttons don't work as expected:**](https://github.com/hobyst/flmidi-kompletekontrol/issues/5) Quantize and toggling automation recording on/off isn't supported yet on the actual MIDI API scope. There's a workaround to get to the quantize buttons by getting into the menus and emulating key pressings but it's slow and buggy. Instead, they switch between windows (browser isn't included on this) and trigger full-screen plugin browser respectively.

## Special thanks

- [Duwayne Wright](https://github.com/soundwrightpro): Coding help

- [B3NYBOI](https://www.youtube.com/channel/UC8C58LOA00jy600kt6h1hTw/): Early testing

- [Tunz Amazin](https://twitter.com/HearMyTunz): Early testing

- [Juanpe](https://www.youtube.com/channel/UC_3ONcvDjAyr1POm2ieefPg/): Early testing

- [Jürgen Moßgraber](https://github.com/git-moss): Implementation reference