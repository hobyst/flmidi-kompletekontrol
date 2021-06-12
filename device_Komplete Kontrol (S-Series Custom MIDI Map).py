# name=Native Instruments Komplete Kontrol (S-Series Custom MIDI Map)

import transport
import midi

def OnMidiIn(event):

    # Fixes pitch wheel issue
    if event.status == 224:
        event.handled = False
        return

    # Fixes aftertouch issue
    elif event.status == 208:
        event.handled = False
        return

    # F4: Creates a new pattern and asks name for it
    elif event.data1 == 112:
        transport.globalTransport(midi.FPT_F4, 1)

    # F5: Playlist
    elif event.data1 == 113:
        transport.globalTransport(midi.FPT_F5, 1)


    # F6: Step sequencer
    elif event.data1 == 114:
        transport.globalTransport(midi.FPT_F6, 1)


    # F7: Piano roll
    elif event.data1 == 115:
        transport.globalTransport(midi.FPT_F7, 1)


    # F8: Plugin picker
    elif event.data1 == 116:
        transport.globalTransport(midi.FPT_F8, 1)


    # F9: Mixer
    elif event.data1 == 117:
        transport.globalTransport(midi.FPT_F9, 1)


    # F10: MIDI settings
    elif event.data1 == 118:
        transport.globalTransport(midi.FPT_F10, 1)


    # F12: Close all windows
    elif event.data1 == 119:
        transport.globalTransport(midi.FPT_F12, 1)
