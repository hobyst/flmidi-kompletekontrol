.. include:: <s5defs.txt>

==============
Basic controls
==============
.. note::
  The buttons on the Komplete Kontrol keyboards and pretty much every Native Instruments device can either be single-function buttons or
  buttons with secondary functions that get reached by using the SHIFT button of the device.

  .. image:: ./_resources/basic_controls/buttons.svg
      :align: center

.. note::
  Any other buttons not listed here aren't available to DAW developers and they are hard locked just to be used with Komplete Kontrol
  or Maschine.

- :green:`PLAY:` Toogle play and pause (will lit up when playback is active)

- :green:`Restart:` Toggle bewteen Pattern playback and Song playback

- :red:`REC:` Toogle recording on/off (will lit up when enabled)

- :red:`Count-In:` Toggle "Countdown before recording" on/off (will lit up when enabled)

- **STOP:** Stops playback and goes to the beginning of the song

- **CLEAR:** Emulates the Delete (Del) button on your keyboard. Active on all windows, actually usable and only lit up when the Piano roll window is focused

- **LOOP:** Toggle "Loop recording" on/off (lit up if enabled)

- **METRO:** Toggle the metronome onn/off (lit up if enabled)

- **TEMPO:** Button for tempo tapping

- **UNDO and REDO:** Self explanatory

- **QUANTIZE:** Doesn't work (`see issue #5 <https://github.com/hobyst/flmidi-kompletekontrol/issues/5>`__). Instead, it switches between windows.

- **AUTO:** Doesn't work (`see issue #5 <https://github.com/hobyst/flmidi-kompletekontrol/issues/5>`__). Instead, it shows the full-screen plugin browser.

- **TRACK (only on A-Series and M-Series):** Switches to the mixer mode when the keyboard is on MIDI mode (SHIFT + PLUG-IN) or is controlling a
  Komplete Kontrol or Maschine instance inside FL Studio.

- **INSTANCE:** Allows manual switching between Komplete Kontrol and Maschine instances. Works on A-Series and M-Series under any condition,
  but on S-Series it is disabled while the DAW integration is enabled since the DAW is supposed to tell the keyboard which instance to focus on.
  Since version 3 of the script, the keyboard will focus whatever instance of Komplete Kontrol is selected on the Channel rack, so the use of the
  INSTANCE button isn't needed.

- **PLUG-IN:** Changes the focus of the keyboard from DAW control mode to Komplete Kontrol mode.

- **MIDI:** Changes to MIDI mode.
