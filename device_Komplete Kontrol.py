# name=Native Instruments Komplete Kontrol
# url=https://github.com/hobyst/flmidi-kompletekontrol/wiki

import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui
import plugins
import channels

import midi
import utils

# Imports Native Instruments Host Integration Agent library
from nihia import nihia

# Imports math library
import math

# Imports the threading module
# threading module isn't supported by FL's interpreter but _thread does
# However, using _thread makes FL crash eventually at launch on Windows and it isn't compatible with the macOS Python interpreter
# Using _dummy_thread instead on macOS and _thread on Windows
import sys

if sys.platform == "win32":
    print("Windows OS detected. Imported _thread module.")
    import _thread

if sys.platform == "darwin":
    print("macOS detected. Imported _dummy_thread module.")
    import lib._dummy_thread as _thread


######################################################################################################################
# User-editable constants for script customization
# Edit this ones to make the script act as you wish
######################################################################################################################

# Modifies the behaviour of the Count-In button
# 
# If set to 0, it will toggle on/off the "Countdown before recording" option on FL Studio
# If set to 1, it will act like on the Maschine software: it will make FL Studio jump straight into record mode with 
# the "Countdown before recording" option enabled
COUNT_IN_BEHAVIOUR = 0

# Tells the script which kind of device are you using
# Possible values: "A_SERIES", "M_SERIES" or "S_SERIES"
DEVICE_SERIES = "S_SERIES"

######################################################################################################################
# Declaration of custom methods, functions and variables
######################################################################################################################

# Variable for the window change produced by the Quantize button
window = -1

# Variable for the window change produced by the Quantize button (second implementation)
window2 = 63

# Method to report mixer tracks
# Splits the 126 mixer busses (including the master) in 15 groups of 8 each one (the last one will have the last two tracks deactivated since 16 * 8 = 128)
# Then shows the tracks corresponding to the ones that are in the same group as the selected track
# 
# Function that retrieves the ID of the track group given the track number is f(x) = 1/8 * x
def updateMixerTracks(dataType: str, selectedTrack: int):
    """ Given the number of the selected track number on the mixer, it is able to know which track group should render into the screen device and bulk reports their information.
    
    ### Parameters

     - dataType: The kind of data you are going to update (PEAK is not valid. Use `updatePeak()` instead)
    
     - trackNumber: The number of the track that is currently selected, going from 0 to 125. `mixer.trackNumber()` can be used directly to fill the argument.
    """

    # Uses the function to know which track group the current track belongs to and truncates the value to get the exact number
    trackGroup = math.trunc(1/8 * selectedTrack)

    # Multiplies the trackGroup to 8 to get the index of the first track that has to be shown
    trackFirst = trackGroup * 8

    # If the selected track belongs to the 16th group, it will declare the last two tracks as non existant
    # Otherwise, it will declare all as existant
    if trackGroup == 15:
        nihia.mixerSendInfo("EXIST", 0, value=1)
        nihia.mixerSendInfo("EXIST", 1, value=1)
        nihia.mixerSendInfo("EXIST", 2, value=1)
        nihia.mixerSendInfo("EXIST", 3, value=1)
        nihia.mixerSendInfo("EXIST", 4, value=1)
        nihia.mixerSendInfo("EXIST", 5, value=1)
        nihia.mixerSendInfo("EXIST", 6, value=0)
        nihia.mixerSendInfo("EXIST", 7, value=0)
    
    else:
        for x in range(trackFirst, trackFirst + 8):
            nihia.mixerSendInfo("EXIST", x - trackFirst, value=1)
    
    
    # In case the group track is the 15th one, it will limit the declaration of tracks to 7
    if trackGroup == 15:
        trackLimit = trackFirst + 7
    
    elif trackGroup != 15:
        trackLimit = trackFirst + 8
    
    # Loop that updates the info of the tracks one by one (sums the actual track number)
    for x in range(trackFirst, trackLimit):
        
        if dataType == "NAME":
            nihia.mixerSendInfo("NAME", x - trackFirst, info=mixer.getTrackName(x))
        
        if dataType == "VOLUME":
            
            # Declares volume as minus infinite if the value is 0
            if mixer.getTrackVolume(x) == 0:
                dB = "-oo"

            elif mixer.getTrackVolume(x) != 0:
                # Calculates the dB value of the current track -- based of a code snippet by soundwrightpro
                dB = (math.exp(mixer.getTrackVolume(x) * 1.25 * math.log(11)) - 1) * 0.1
                dB = round(math.log10(dB) * 20, 1)

            dB = str(dB) + " dB"
            
            nihia.mixerSendInfo("VOLUME", x - trackFirst, info=dB)
    
        if dataType == "PAN":
            # Centered
            if math.trunc(mixer.getTrackPan(x)) == 0:
                nihia.mixerSendInfo("PAN", x - trackFirst, info="Centered")
            
            # Right
            if mixer.getTrackPan(x) > 0:
                nihia.mixerSendInfo("PAN", x - trackFirst, info=str(round((abs(mixer.getTrackPan(x)) * 100))) + "% " + "Right")

            # Left
            if mixer.getTrackPan(x) < 0:
                nihia.mixerSendInfo("PAN", x - trackFirst, info=str(round((abs(mixer.getTrackPan(x)) * 100))) + "% " + "Left")

        if dataType == "IS_MUTE":
            nihia.mixerSendInfo("IS_MUTE", x - trackFirst, value=mixer.isTrackMuted(x))
        
        if dataType == "IS_SOLO":
            nihia.mixerSendInfo("IS_SOLO", x - trackFirst, value=mixer.isTrackSolo(x))

        if dataType == "SELECTED":
            nihia.mixerSendInfo("SELECTED", x - trackFirst, value=mixer.isTrackSelected(x))
        
        if dataType == "VOLUME_GRAPH":
            nihia.mixerSetGraph(x - trackFirst, "VOLUME", mixer.getTrackVolume(x))
        
        if dataType == "PAN_GRAPH":
            nihia.mixerSetGraph(x - trackFirst, "PAN", mixer.getTrackPan(x))


    # Checks the track group once more to clean up the last two tracks
    if trackGroup == 15:
        if dataType == "NAME":
            nihia.mixerSendInfo("NAME", 6, info="")
            nihia.mixerSendInfo("NAME", 7, info="")
        
        # Track 7 --> Current
        if dataType == "VOLUME":
            nihia.mixerSendInfo("VOLUME", 6, info=" ")
            nihia.mixerSendInfo("VOLUME", 7, info=" ")
        
        if dataType == "PAN":
            nihia.mixerSendInfo("PAN", 6, info=" ")
            nihia.mixerSendInfo("PAN", 7, info=" ")
        
        if dataType == "IS_MUTE":
            nihia.mixerSendInfo("IS_MUTE", 6, value=0)
            nihia.mixerSendInfo("IS_MUTE", 7, value=0)
        
        if dataType == "IS_SOLO":
            nihia.mixerSendInfo("IS_SOLO", 6, value=0)
            nihia.mixerSendInfo("IS_SOLO", 7, value=0)

        if dataType == "VOLUME_GRAPH":
            nihia.mixerSetGraph(6, "VOLUME", 0)
            nihia.mixerSetGraph(7, "VOLUME", 0)
        
        if dataType == "PAN_GRAPH":
            nihia.mixerSetGraph(6, "PAN", 0)
            nihia.mixerSetGraph(7, "PAN", 0)


def updateMixer():
    """ Updates every property of the mixer of the deivce but the peak values. """
    updateMixerTracks("NAME",mixer.trackNumber())
    updateMixerTracks("SELECTED",mixer.trackNumber())
    updateMixerTracks("VOLUME",mixer.trackNumber())
    updateMixerTracks("PAN",mixer.trackNumber())
    updateMixerTracks("IS_MUTE",mixer.trackNumber())
    updateMixerTracks("IS_SOLO",mixer.trackNumber())

    # Update fader visualization on S-Series keyboards
    if DEVICE_SERIES == "S_SERIES":
        updateMixerTracks("VOLUME_GRAPH",mixer.trackNumber())
        updateMixerTracks("PAN_GRAPH",mixer.trackNumber())


def adjustMixer(knob: int, dataType: str, action: str, selectedTrack: int):
    """ Dynamically maps the physical knob to the right mixer track depending on the track group the selected track belongs to, and adjusts the parameter.
    ### Parameters

     - knob: From 0 to 7. Number of the physical knob you are mapping.
    
     - dataType: The parameter you are going to adjust. Can be PAN or VOLUME.

     - action: Can be INCREASE or DECREASE.

     - selectedTrack: The actual selected track that will be used to calculate the track group.
    """
    # Calculates which track group the current track belongs to and truncates the value to get the exact number
    trackGroup = math.trunc(1/8 * selectedTrack)

    # Multiplies the trackGroup to 8 to get the index of the first track of that group
    trackFirst = trackGroup * 8

    if dataType == "VOLUME":
        if action == "INCREASE":
            mixer.setTrackVolume(trackFirst + knob, mixer.getTrackVolume(trackFirst + knob) + 0.02)
        
        if action == "DECREASE":
            mixer.setTrackVolume(trackFirst + knob, mixer.getTrackVolume(trackFirst + knob) - 0.02)

    if dataType == "PAN":
        if action == "INCREASE":
            mixer.setTrackPan(trackFirst + knob, mixer.getTrackPan(trackFirst + knob) + 0.01)

        if action == "DECREASE":
            mixer.setTrackPan(trackFirst + knob, mixer.getTrackPan(trackFirst + knob) - 0.01)


def encoderHandler(axis: str) -> int:
    """ Allows to handle the inversion of axis of the 4D Encoder that happens between A/M-Series devices and S-Series devices, by 
    returning the right MIDI value FL Studio has to check for.
    ### Parameters
     - axis: The axis you want to get the value for.
    """
    devices = {
        "A_SERIES": 1,
        "M_SERIES": 1,
        "S_SERIES": 2
    }

    device = devices.get(DEVICE_SERIES)

    # Device check
    if device == 1:
        # X axis
        if axis == "X":
           return nihia.buttons.get("ENCODER_X_A")
        
        # Y axis
        if axis == "Y":
           return nihia.buttons.get("ENCODER_Y_A")

    if device == 2:
        # X axis
        if axis == "X":
           return nihia.buttons.get("ENCODER_X_S")
        
        # Y axis
        if axis == "Y":
           return nihia.buttons.get("ENCODER_Y_S")


def mixerMuteSoloHandler(action: str, targetTrack: int, selectedTrack: int):
    """ Handles the way mixer and solo commands are sent from S-Series keyboards. 
    ### Parameters
    
     - action: MUTE or SOLO.
     - targetTrack: From 0 to 7, the track that the user is trying to mute or solo from the ones showing on the device's mixer.
     - selectedTrack: The currently selected track that is used to calculate the track group.
    """
    # Uses the function to know which track group the current track belongs to and truncates the value to get the exact number
    trackGroup = math.trunc(1/8 * selectedTrack)

    # Multiplies the trackGroup to 8 to get the index of the first track that has to be shown
    trackFirst = trackGroup * 8

    # Adjusts the correct property of the right track
    if action == "MUTE":
        mixer.muteTrack(trackFirst + targetTrack)

    if action == "SOLO":
        mixer.soloTrack(trackFirst + targetTrack)


def updatePeak(selectedTrack: int):
    """ Updates peak values for the tracks showing on the device. 
    ### Parameters

     - selectedTrack: The currently selected track.
    """

    # Uses the function to know which track group the current track belongs to and truncates the value to get the exact number
    trackGroup = math.trunc(1/8 * selectedTrack)

    # Multiplies the trackGroup to 8 to get the index of the first track that has to be shown
    trackFirst = trackGroup * 8

    # Creates peakList if peak values are going to be updated
    peakList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # In case the group track is the 15th one, it will limit the declaration of tracks to 7
    if trackGroup == 15:
        trackLimit = trackFirst + 7
    
    elif trackGroup != 15:
        trackLimit = trackFirst + 8

    # Gets the 16 peak values that need to be reported to the device by building a list [peakL_0, peakR_0, peakL_1, peakR_1 ...]
    for x in range(trackFirst, trackLimit):
        peakList[(x - trackFirst) * 2] = mixer.getTrackPeaks(x, midi.PEAK_L)
        peakList[(x - trackFirst) * 2 + 1] = mixer.getTrackPeaks(x, midi.PEAK_R)

    # Sends the values to the device
    nihia.mixerSendInfo("PEAK", 0, peakValues = peakList)


def detectDevice():
    """ Gets the MIDI device name from FL Studio and sets `DEVICE_SERIES` to the right value in order for the script to work properly. """

    # Imports DEVICE_SERIES from the global scope
    global DEVICE_SERIES

    # Retrieves the device name from FL Studio
    deviceName = device.getName()

    # Saves the 22th character of the device name for the S-Series check to isolate the extraction and avoid errors stopping the execution of the script
    char21 = None
    try:
        char21 = deviceName[21]
    except:
        char21 = None

    # Sets DEVICE_NAME depending on the retrieved name
    if deviceName == "Komplete Kontrol A DAW":
        DEVICE_SERIES = "A_SERIES"
        print("Detected device: Komplete Kontrol A-Series")
    
    elif deviceName == "Komplete Kontrol M DAW":
        DEVICE_SERIES = "M_SERIES"
        print("Detected device: Komplete Kontrol M-Series")
    
    elif char21 == "-":     # Gets the 18th char on the name to see if it matches the "Komplete Kontrol DAW - X" naming scheme S-Series devices follow
        DEVICE_SERIES = "S_SERIES"
        print("Detected device: Komplete Kontrol S-Series")
    
    else:
        print("Device detection failed. Going with the manually specified device on the script:", DEVICE_SERIES)


######################################################################################################################
# Button to action definitions
######################################################################################################################

def OnMidiIn(event):
    """ Wrapper for the OnMidiIn thread. """
    # Play button
    if event.data1 == nihia.buttons.get("PLAY"):
        event.handled = True
        transport.start()

    # Restart button
    elif event.data1 == nihia.buttons.get("RESTART"):
        event.handled = True
        transport.setLoopMode()

    # Record button
    elif event.data1 == nihia.buttons.get("REC"):
        event.handled = True
        transport.record()
    
    # Count-In button
    elif event.data1 == nihia.buttons.get("COUNT_IN"):
        event.handled = True
        
        # Defines the standard behaviour (just to toggle "Countdown before recording" on/off)
        if COUNT_IN_BEHAVIOUR == 0:
            transport.globalTransport(midi.FPT_CountDown, 1)
        
        # Defines behaviour of the button if the user chooses the Maschine-alike behaviour
        if COUNT_IN_BEHAVIOUR == 1:
    
            # Toggles recording on if it isn't enabled already
            if transport.isRecording() == 0:
                transport.record()
            
            # Toggles countdown before recording on if it isn't enabled already
            if ui.isPrecountEnabled() == 0:
                transport.globalTransport(midi.FPT_CountDown, 1)
            
            # Stops playback if FL Studio is playing
            if transport.isPlaying() == True:
                transport.stop()
            
            # Then turns playback on again. This time record and countdown before recording will be activated
            transport.start()

    # Stop button
    elif event.data1 == nihia.buttons.get("STOP"):
        event.handled = True
        transport.stop()

    # Clear button
    # This one in other DAWs (in Maschine, specifically) this button is meant to clear the MIDI clip you're
    # on so you can record again on it without having to use a mouse to delete all of the notes on the clip before
    # recording again
    #
    # However, since the MIDI API on FL Studio doesn't allow control over the piano roll specifically, for now it will only just
    # emulate the delete button (which does the same)
    elif event.data1 == nihia.buttons.get("CLEAR"):
        event.handled = True
        ui.delete()
    
    # Loop button (toggles loop recording on/off)
    elif event.data1 == nihia.buttons.get("LOOP"):
        event.handled = True
        transport.globalTransport(midi.FPT_LoopRecord, 1)

    # Metronome button
    elif event.data1 == nihia.buttons.get("METRO"):
        event.handled = True
        transport.globalTransport(midi.FPT_Metronome, 1)
    
    # Tempo button
    elif event.data1 == nihia.buttons.get("TEMPO"):
        event.handled = True
        transport.globalTransport(midi.FPT_TapTempo, 1)


    # Undo button
    elif event.data1 == nihia.buttons.get("UNDO"):
        event.handled = True
        general.undoUp()
    
    # Redo button
    elif event.data1 == nihia.buttons.get("REDO"):
        event.handled = True
        general.undo()

    
    # Quantize button
    # TODO: Not imlpemented yet in FL Studio MIDI API
    # 
    # Instead, it changes between FL windows
    # TODO: The code is correctly written, but the ui.showWindow() method has a bug that causes the Piano roll and Browser windows not to
    # appear when invoked. It has been said it should be fixed in a future update.
    # -----------------------------------------------------------------------------------------------------------------------------------
    # if event.data1 == nihia.buttons.get("QUANTIZE"):
    #     global window
    #     window += 1

    #     if window <= 4:
    #         ui.showWindow(window)
    #         print("if reached")
    #     elif window > 4:
    #         window = 0
    #         ui.showWindow(window)
    # -----------------------------------------------------------------------------------------------------------------------------------
    # 
    # Alternative implementation: Emulate the Fn buttons
    elif event.data1 == nihia.buttons.get("QUANTIZE"):
        event.handled = True
        global window2
        window2 += 1

        # Normal behaviour if the action ID is between the desired range
        if window2 <= 68 and window2 != 67:
            transport.globalTransport(window2, 1)
        
        # Skips the 67 value which calls the full screen plugin picker and calls the mixer instead
        elif window2 == 67:
            window2 += 1
            transport.globalTransport(window2, 1)

        # Once window value is out of range, it sets it again to the first value in range
        elif window2 > 68:
            window2 = 64
            transport.globalTransport(window2, 1)


    # Automation button
    # Enables and disables the recording automation events
    # TODO: Not implemented yet in FL Studio MIDI API
    # 
    # Instead, it shows the full-screen plugin browser
    elif event.data1 == nihia.buttons.get("AUTO"):
        event.handled = True
        transport.globalTransport(midi.FPT_F8, 1)


    # Mute button - A-Series
    elif event.data1 == nihia.buttons.get("MUTE_SELECTED"):
        event.handled = True
        mixer.muteTrack(mixer.trackNumber())

    # Solo button - A-Series
    elif event.data1 == nihia.buttons.get("SOLO_SELECTED"):
        event.handled = True
        mixer.soloTrack(mixer.trackNumber())

    # Mute button - S-Series
    elif event.data1 == nihia.buttons.get("MUTE"):
        event.handled = True
        mixerMuteSoloHandler("MUTE", event.data2, mixer.trackNumber())

    # Solo button - S-Series
    elif event.data1 == nihia.buttons.get("SOLO"):
        event.handled = True
        mixerMuteSoloHandler("SOLO", event.data2, mixer.trackNumber())



    # 4D Encoder +
    elif event.data1 == nihia.buttons.get("ENCODER_GENERAL") and event.data2 == nihia.buttons.get("PLUS"):
        event.handled = True
        
        # Mixer navigation (right)
        if ui.getFocused(midi.widMixer) == True:
            ui.right()
        
        # Playback jogging
        elif (ui.getFocused(midi.widPianoRoll) == True) or (ui.getFocused(midi.widPlaylist) == True):
            transport.setSongPos(transport.getSongPos(midi.SONGLENGTH_S) + 1, midi.SONGLENGTH_S)

        # General navigation
        else:
            ui.down()
    
    # 4D Encoder -
    elif event.data1 == nihia.buttons.get("ENCODER_GENERAL") and event.data2 == nihia.buttons.get("MINUS"):
        event.handled = True
        
        # Mixer navigation
        if ui.getFocused(midi.widMixer) == True:
            ui.left()

        elif (ui.getFocused(midi.widPianoRoll) == True) or (ui.getFocused(midi.widPlaylist) == True):
            transport.setSongPos(transport.getSongPos(midi.SONGLENGTH_S) - 1, midi.SONGLENGTH_S)

        # General navigation
        else:
            ui.up()
    
    # 4D Encoder + (selected track volume)
    elif event.data1 == nihia.buttons.get("ENCODER_VOLUME_SELECTED") and event.data2 == nihia.buttons.get("PLUS"):
        event.handled = True
        mixer.setTrackVolume(mixer.trackNumber(), mixer.getTrackVolume(mixer.trackNumber()) + 0.01)
    
    # 4D Encoder - (selected track volume)
    elif event.data1 == nihia.buttons.get("ENCODER_VOLUME_SELECTED") and event.data2 == nihia.buttons.get("MINUS"):
        event.handled = True
        mixer.setTrackVolume(mixer.trackNumber(), mixer.getTrackVolume(mixer.trackNumber()) - 0.01)

    
    # 4D Encoder + (selected track pan)
    elif event.data1 == nihia.buttons.get("ENCODER_PAN_SELECTED") and event.data2 == nihia.buttons.get("PLUS"):
        event.handled = True
        mixer.setTrackPan(mixer.trackNumber(), mixer.getTrackPan(mixer.trackNumber()) + 0.01)
    
    # 4D Encoder + (selected track pan)
    elif event.data1 == nihia.buttons.get("ENCODER_PAN_SELECTED") and event.data2 == nihia.buttons.get("MINUS"):
        event.handled = True
        mixer.setTrackPan(mixer.trackNumber(), mixer.getTrackPan(mixer.trackNumber()) - 0.01)
    
    # 4D Encoder up
    elif event.data1 == encoderHandler("Y") and event.data2 == nihia.buttons.get("UP"):
        event.handled = True
        ui.up()

    # 4D Encoder down 
    elif event.data1 == encoderHandler("Y") and event.data2 == nihia.buttons.get("DOWN"):
        event.handled = True
        ui.down()

    # 4D Encoder (using FPT because ui.left doesn't work on the playlist)
    elif event.data1 == encoderHandler("X") and event.data2 == nihia.buttons.get("LEFT"):
        event.handled = True
        if ui.getFocused(midi.widMixer) == True:
            # This one doesn't move the mixer view as you get to the border
            # ----------------------------------------------------
            # mixer.setTrackNumber(mixer.trackNumber() - 1)
            # ----------------------------------------------------
            ui.left()


        else:
            ui.left()

    # 4D Encoder (using FPT because ui.right doesn't work on the playlist)
    elif event.data1 == encoderHandler("X") and event.data2 == nihia.buttons.get("RIGHT"):
        event.handled = True
        if ui.getFocused(midi.widMixer) == True:
            # This one doesn't move the mixer view as you get to the border
            # ----------------------------------------------------
            # mixer.setTrackNumber(mixer.trackNumber() + 1)
            # ----------------------------------------------------
            ui.right()
        
        else:
            ui.right()


    # 4D Encoder button
    elif event.data1 == nihia.buttons.get("ENCODER_BUTTON"):
        event.handled = True
        ui.enter()
    
    # 4D Encoder button (shifted)
    elif event.data1 == nihia.buttons.get("ENCODER_BUTTON_SHIFTED"):
        event.handled = True
        transport.globalTransport(midi.FPT_Menu, 1)

    # Knobs
    # Normal knobs - increase values
    elif event.data1 == nihia.knobs.get("KNOB_1A") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(0, "VOLUME", "INCREASE", mixer.trackNumber())
    
    elif event.data1 == nihia.knobs.get("KNOB_2A") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(1, "VOLUME", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_3A") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(2, "VOLUME", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_4A") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(3, "VOLUME", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_5A") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(4, "VOLUME", "INCREASE", mixer.trackNumber())
    
    elif event.data1 == nihia.knobs.get("KNOB_6A") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(5, "VOLUME", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_7A") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        # Handles track group 15 exception
        if math.trunc(1/8 * mixer.trackNumber()) == 15:
            return
        else:    
            adjustMixer(6, "VOLUME", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_8A") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        # Handles track group 15 exception
        if math.trunc(1/8 * mixer.trackNumber()) == 15:
            return
        else: 
            adjustMixer(7, "VOLUME", "INCREASE", mixer.trackNumber())
    
    # Normal knobs - decrease values
    elif event.data1 == nihia.knobs.get("KNOB_1A") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(0, "VOLUME", "DECREASE", mixer.trackNumber())
    
    elif event.data1 == nihia.knobs.get("KNOB_2A") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(1, "VOLUME", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_3A") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(2, "VOLUME", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_4A") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(3, "VOLUME", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_5A") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(4, "VOLUME", "DECREASE", mixer.trackNumber())
    
    elif event.data1 == nihia.knobs.get("KNOB_6A") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(5, "VOLUME", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_7A") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        # Handles track group 15 exception
        if math.trunc(1/8 * mixer.trackNumber()) == 15:
            return
        else: 
            adjustMixer(6, "VOLUME", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_8A") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        # Handles track group 15 exception
        if math.trunc(1/8 * mixer.trackNumber()) == 15:
            return
        else: 
            adjustMixer(7, "VOLUME", "DECREASE", mixer.trackNumber())


    
    # Shifted knobs - increase values
    elif event.data1 == nihia.knobs.get("KNOB_1B") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(0, "PAN", "INCREASE", mixer.trackNumber())
    
    elif event.data1 == nihia.knobs.get("KNOB_2B") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(1, "PAN", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_3B") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(2, "PAN", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_4B") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(3, "PAN", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_5B") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(4, "PAN", "INCREASE", mixer.trackNumber())
    
    elif event.data1 == nihia.knobs.get("KNOB_6B") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        adjustMixer(5, "PAN", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_7B") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        # Handles track group 15 exception
        if math.trunc(1/8 * mixer.trackNumber()) == 15:
            return
        else: 
            adjustMixer(6, "PAN", "INCREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_8B") and event.data2 == nihia.knobs.get("INCREASE"):
        event.handled = True
        # Handles track group 15 exception
        if math.trunc(1/8 * mixer.trackNumber()) == 15:
            return
        else: 
            adjustMixer(7, "PAN", "INCREASE", mixer.trackNumber())
    
    # Shifted knobs - decrease values
    elif event.data1 == nihia.knobs.get("KNOB_1B") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(0, "PAN", "DECREASE", mixer.trackNumber())
    
    elif event.data1 == nihia.knobs.get("KNOB_2B") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(1, "PAN", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_3B") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(2, "PAN", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_4B") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(3, "PAN", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_5B") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(4, "PAN", "DECREASE", mixer.trackNumber())
    
    elif event.data1 == nihia.knobs.get("KNOB_6B") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        adjustMixer(5, "PAN", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_7B") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        # Handles track group 15 exception
        if math.trunc(1/8 * mixer.trackNumber()) == 15:
            return
        else: 
            adjustMixer(6, "PAN", "DECREASE", mixer.trackNumber())

    elif event.data1 == nihia.knobs.get("KNOB_8B") and event.data2 == nihia.knobs.get("DECREASE"):
        event.handled = True
        # Handles track group 15 exception
        if math.trunc(1/8 * mixer.trackNumber()) == 15:
            return
        else: 
            adjustMixer(7, "PAN", "DECREASE", mixer.trackNumber())
    
######################################################################################################################
# Script logic
######################################################################################################################

def OnInit():
    # Detects the device the script is running on
    detectDevice()
    
    # Tells to FL Studio the device has peak meters
    device.setHasMeters()

    # Activates the deep integration mode
    nihia.handShake()

    # Sets the lights on
    nihia.buttonSetLight("PLAY", 0)
    nihia.buttonSetLight("REC", 0)
    nihia.buttonSetLight("COUNT_IN", 0)
    nihia.buttonSetLight("STOP", 0)
    nihia.buttonSetLight("CLEAR", 1)
    nihia.buttonSetLight("LOOP", 0)
    nihia.buttonSetLight("METRO", 0)
    nihia.buttonSetLight("UNDO", 1)
    nihia.buttonSetLight("REDO", 1)
    nihia.buttonSetLight("QUANTIZE", 1)
    nihia.buttonSetLight("REDO", 1)
    nihia.buttonSetLight("TEMPO", 1)

    # Sets the lights of the 4D Encoder on S-Series keyboards on
    if DEVICE_SERIES == "S_SERIES":
        nihia.buttonSetLight("ENCODER_X_S", 1)
        nihia.buttonSetLight("ENCODER_X_S", 127)
        nihia.buttonSetLight("ENCODER_Y_S", 1)
        nihia.buttonSetLight("ENCODER_Y_S", 127)

    # Updates the device mixer
    updateMixer()

def OnDeInit():
    # Deactivates the deep integration mode
    nihia.goodBye()


# def OnUpdateBeatIndicator(value):
    # Play button blinking -- code snippet based on one from soundwrightpro
    # Decided to remove it in order to have a pure implementation of the features given by Native Instruments
    # -------------------------------------------------------------------------------------------------------
    #  if transport.isPlaying() == True:
    #     # Make it turn on on beat change
    #     if value == 2:
    #         nihia.buttonSetLight("PLAY", 1)
    #     # Make it turn on on bar change
    #     elif value == 1:
    #         nihia.buttonSetLight("PLAY", 1)
    #     # Make it turn off when there is no change
    #     else:
    #         nihia.buttonSetLight("PLAY", 0)
    # -------------------------------------------------------------------------------------------------------


def TOnIdle():
    """ Wrapper for the OnInit thread. """
    # Updates the LED of the CLEAR button (moved to OnIdle, since OnRefresh isn't called when focused window changes)
    if ui.getFocused(midi.widPianoRoll) == True:
        nihia.buttonSetLight("CLEAR", 1)
    
    elif ui.getFocused(midi.widPianoRoll) == False:
        nihia.buttonSetLight("CLEAR", 0)

def OnIdle():
    _thread.start_new_thread(TOnIdle, ())


# Updates the LEDs and the mixer
def TOnRefresh(HW_Dirty_LEDs):
    """ Wrapper for the OnRefresh thread. """
    # PLAY button
    if transport.isPlaying() == True:
        nihia.buttonSetLight("PLAY", 1)
    
    elif transport.isPlaying() == False:
        nihia.buttonSetLight("PLAY", 0)
    
    # STOP button
    if transport.isPlaying() == True:
        nihia.buttonSetLight("STOP", 0)
    
    elif transport.isPlaying() == False:
        nihia.buttonSetLight("STOP", 1)
    
    # REC button
    if transport.isRecording() == True:
        nihia.buttonSetLight("REC", 1)
    
    elif transport.isRecording() == False:
        nihia.buttonSetLight("REC", 0)

    # COUNT-IN button
    if ui.isPrecountEnabled() == True:
        nihia.buttonSetLight("COUNT_IN", 1)

    elif ui.isPrecountEnabled() == False:
        nihia.buttonSetLight("COUNT_IN", 0)
    
    # CLEAR button (moved to OnIdle, since OnRefresh isn't called when focused window changes)

    # LOOP button
    if ui.isLoopRecEnabled() == True:
        nihia.buttonSetLight("LOOP", 1)
    
    elif ui.isLoopRecEnabled() == False:
        nihia.buttonSetLight("LOOP", 0)

    # METRO button
    if ui.isMetronomeEnabled() == True:
        nihia.buttonSetLight("METRO", 1)

    elif ui.isMetronomeEnabled() == False:
        nihia.buttonSetLight("METRO", 0)

    # MUTE button
    if mixer.isTrackMuted(mixer.trackNumber()) == True:
        nihia.buttonSetLight("MUTE_SELECTED", 1)

    elif mixer.isTrackMuted(mixer.trackNumber()) == False:
        nihia.buttonSetLight("MUTE_SELECTED", 0)
    
    # SOLO button
    if mixer.isTrackSolo(mixer.trackNumber()) == True:
        nihia.buttonSetLight("SOLO_SELECTED", 1)

    elif mixer.isTrackSolo(mixer.trackNumber()) == False:
        nihia.buttonSetLight("SOLO_SELECTED", 0)
    
    # Update mixer but peak meters
    updateMixer()

    # Tell the device if a mixer track is selected or not
    # It enables the ability to control mixer tracks using the 4D Encoder on S-Series keyboards
    # Disabled due to lack of awareness on how it is enabled and disabled correctly
    # if ui.getFocused(midi.widMixer) == True:
    #     nihia.mixerSendInfoSelected("SELECTED", "GENERIC")
    # 
    # if ui.getFocused(midi.widMixer) == False:
    #     nihia.mixerSendInfoSelected("SELECTED", "EMPTY")

    # Check if the selected plugin is a Komplete Kontrol instance
    if (plugins.isValid(channels.channelNumber()) == True): # Checks if plugin exists
        # If it does, sends the instance ID
        if plugins.getPluginName(channels.channelNumber()) == "Komplete Kontrol":
            nihia.mixerSendInfo("KOMPLETE_INSTANCE", 0, info=plugins.getParamName(0, channels.channelNumber()))
        
        # If it doesn't, tells the keyboard about it
        else:
            nihia.mixerSendInfo("KOMPLETE_INSTANCE", 0, info="")

    else:
        nihia.mixerSendInfo("KOMPLETE_INSTANCE", 0, info="")

def OnRefresh(HW_Dirty_LEDs):
    _thread.start_new_thread(TOnRefresh, (HW_Dirty_LEDs,))


def TOnUpdateMeters():
    """ Wrapper for the OnUpdateMeters thread. """
    # Update peak meters
    # TODO: Disabled due to performance issues (multi-threading support needed)
    # ----------------------------------------------
    if DEVICE_SERIES == "S_SERIES":
      updatePeak(mixer.trackNumber())
    # ----------------------------------------------

def OnUpdateMeters():
    _thread.start_new_thread(TOnUpdateMeters, ())