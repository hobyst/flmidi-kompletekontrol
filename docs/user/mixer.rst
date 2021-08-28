=====
Mixer
=====

The mixer in the Komplete Kontrol keyboards is accessed the same way as with any other of the officially supported DAWs:
by using the MIXER button on S-Series MK2 keyboards or the TRACK button on A-Series and M32 keyboards.

The mixer tracks shown in the device come from dividing the FL Studio mixer in groups of 8 starting from the mixer and
guessing which group to show depending on the currently selected mixer track. You can use the 4D Encoder of the keyboard
to navigate between different mixer tracks.

Volume and pan
==============

S-Series MK2
------------

By default, the knobs will change the volume of the track they have right on top on the display. Press SHIFT + 4D Encoder 🔼
and SHIFT + 4D Encoder 🔽 to toggle between volume and pan adjustment. You can also use a knob while holding SHIFT for more
fine adjustments.

A-Series and M32
----------------

By default, the knobs will change the volume of the track they have right on top with the display only showing the currently selected
track information. Use the touch sensitivity of the knobs by just laying a finger on top of a knob to reveal the information of the
track it controls on the device display, twist it to adjust volume and twist it while pressing SHIFT to adjust pan.

.. tip::
    Indifferently of the device, you can adjust the volume and pan increments right in the ``config.py`` file and
    looking for this piece of code:

    .. code-block:: python

        # Knob increments
        # These values set the amount of increments for each message your keyboard sends to FL Studio
        # when twisting the knobs on your device to change track volume and pan on the mixer
        # Defaults are:
        # - KNOB_INCREMENTS_VOL = 0.02
        # - KNOB_INCREMENTS_PAN = 0.02
        KNOB_INCREMENTS_VOL = 0.02
        KNOB_INCREMENTS_PAN = 0.02

Mute and solo
=============

S-Series MK2
------------

Pressing the M or S buttons on your keyboard will mute or solo the currently selected track. To mute or solo multiple tracks at once,
hold one of the M or S buttons and then hit the white buttons right on top of the mixer tracks you want to mute or solo.

A-Series and M32
----------------

To mute or solo the currently selected track, hold SHIFT and press either ◀ or ▶ to reach the mute and solo buttons.

These keyboards don't support mute or solo for multiple tracks at once like the S-Series MK2 does.

Track selection
===============

S-Series MK2
------------

Use the buttons on top of the displays of the keyboard to select and deselect mixer tracks.

A-Series and M32
----------------

These models don't support track selection. Only one track will be selected at a time and it will be the same
that gets shown in the display.
