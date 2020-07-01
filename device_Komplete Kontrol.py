# name=Native Instruments Komplete Kontrol
# url = 

import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui

import midi
import utils

# Imports Native Instruments Host Integration Agent library
from nihia import nihia

# Imports math library
import math


######################################################################################################################
# User-editable constants for script customization
# Edit this ones to make the script act as you wish
######################################################################################################################

# Modifies the behaviour of the Count-In button
# 
# If set to 0, it will toggle on/off the "Countdown before recording" option on FL Studio
# If set to 1, it will act like on the Maschine software: it will make FL Studio jump straight into record mode with 
# the "Countdown before recording" option enabled
COUNT_IN_BEHAVIOUR=0


######################################################################################################################
# Declaration of custom methods, functions and variables
######################################################################################################################

# Variable for the window change produced by the Quantize button
window = -1

# Variable for the window change produced by the Quantize button (second implementation)
window2 = 63

# Method to report mixer tracks
# Splits the 126 mixer busses (including the master) in 16 groups of 8 each one (the last one will have the last two tracks deactivated since 16 * 8 = 128)
# Then shows the tracks corresponding to the ones that are in the same group as the selected track
# 
# Function that retrieves the ID of the track group given the track number is f(x) = 1/8 * x
def updateMixerTracks(dataType: str, trackNumber: int):
    """ Given the number of the selected track number on the mixer, it is able to know which track group should render into the screen device and bulk reports their information.
    
    ### Parameters

     - dataType: The kind of data you are going to update.
    
     - trackNumber: The number of the track that is currently selected, going from 0 to 125. `mixer.trackNumber()` can be used directly to fill the argument.
    """

    # Uses the function to know which track group the current track belongs to and truncates the value to get the exact number
    trackGroup = math.trunc(1/8 * trackNumber)

    # Multiplies the trackGroup to 8 to get the index of the first track that has to be shown
    trackFirst = trackGroup * 8

    
    # If the selected track belongs to the 16th group, it will declare the last two tracks as non existant
    # Otherwise, it will declare all as existant
    if trackGroup == 15:
        for x in range(trackFirst, trackFirst + 8):
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
    
    
    # In case the group track is the 16th one, it will limit the declaration of tracks to 7
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
            if mixer.getTrackPan(x) == 0:
                nihia.mixerSendInfo("PAN", x - trackFirst, info="Centered")
            
            # Right
            elif mixer.getTrackPan(x) > 1:
                nihia.mixerSendInfo("PAN", x - trackFirst, info=str(round((abs(mixer.getTrackPan(x)) * 100))) + "% Right")

            # Left
            elif mixer.getTrackPan(x) < 1:
                nihia.mixerSendInfo("PAN", x - trackFirst, info=str(round((abs(mixer.getTrackPan(x)) * 100))) + "% " + "Left")

        if dataType == "IS_MUTE":
            nihia.mixerSendInfo("IS_MUTE", x - trackFirst, value=mixer.isTrackMuted(x))
        
        if dataType == "IS_SOLO":
            nihia.mixerSendInfo("IS_SOLO", x - trackFirst, value=mixer.isTrackSolo(x))

        if dataType == "SELECTED":
            nihia.mixerSendInfo("SELECTED", x - trackFirst, value=mixer.isTrackSelected(x))
        
        if dataType == "PEAK":
            nihia.mixerSendInfo("PEAK", x - trackFirst, info=[mixer.getTrackPeaks(x, 0), mixer.getTrackPeaks(x, 1)])


def updateMixer():
    """ Updates every property of the mixer but the peak values. """
    updateMixerTracks("NAME",mixer.trackNumber())
    updateMixerTracks("SELECTED",mixer.trackNumber())
    updateMixerTracks("VOLUME",mixer.trackNumber())
    updateMixerTracks("PAN",mixer.trackNumber())
    updateMixerTracks("IS_MUTE",mixer.trackNumber())
    updateMixerTracks("IS_SOLO",mixer.trackNumber())


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
            mixer.setTrackVolume(trackFirst + knob, mixer.getTrackVolume(trackFirst + knob) + 0.005)
        
        if action == "DECREASE":
            mixer.setTrackVolume(trackFirst + knob, mixer.getTrackVolume(trackFirst + knob) - 0.005)

    if dataType == "PAN":
        if action == "INCREASE":
            mixer.setTrackPan(trackFirst + knob, mixer.getTrackPan(trackFirst + knob) + 0.01)

        if action == "DECREASE":
            mixer.setTrackPan(trackFirst + knob, mixer.getTrackPan(trackFirst + knob) - 0.01)


######################################################################################################################
# Button to action definitions
######################################################################################################################

def OnMidiIn(event):
    # Play button
    if event.data1 == nihia.buttons.get("PLAY"):
        transport.start()

    # Restart button
    if event.data1 == nihia.buttons.get("RESTART"):
        transport.stop()
        transport.start()

    # Record button
    if event.data1 == nihia.buttons.get("REC"):
        transport.record()
    
    # Count-In button
    if event.data1 == nihia.buttons.get("COUNT_IN"):
        
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
    if event.data1 == nihia.buttons.get("STOP"):
        transport.stop()

    # Clear button
    # This one in other DAWs (in Maschine, specifically) this button is meant to clear the MIDI clip you're
    # on so you can record again on it without having to use a mouse to delete all of the notes on the clip before
    # recording again
    #
    # However, since the MIDI API on FL Studio doesn't allow control over the piano roll specifically, for now it will only just
    # emulate the delete button (which does the same)
    if event.data1 == nihia.buttons.get("CLEAR"):
        ui.delete()
    
    # Loop button (toggles loop recording on/off)
    if event.data1 == nihia.buttons.get("LOOP"):
        transport.globalTransport(midi.FPT_LoopRecord, 1)

    # Metronome button
    if event.data1 == nihia.buttons.get("METRO"):
        transport.globalTransport(midi.FPT_Metronome, 1)
    
    # Tempo button
    if event.data1 == nihia.buttons.get("TEMPO"):
        transport.globalTransport(midi.FPT_TapTempo, 1)


    # Undo button
    if event.data1 == nihia.buttons.get("UNDO"):
        general.undoUp()
    
    # Redo button
    if event.data1 == nihia.buttons.get("REDO"):
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
    if event.data1 == nihia.buttons.get("QUANTIZE"):
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
    if event.data1 == nihia.buttons.get("AUTO"):
        transport.globalTransport(midi.FPT_F8, 1)


    # Mute button
    if event.data1 == nihia.buttons.get("MUTE"):
        mixer.muteTrack(mixer.trackNumber())

    # Solo button
    if event.data1 == nihia.buttons.get("SOLO"):
        mixer.soloTrack(mixer.trackNumber())


    # 4D Encoder + to down (to improve navigation in general)
    if event.data1 == nihia.buttons.get("ENCODER_PLUS")[0] and event.data2 == nihia.buttons.get("ENCODER_PLUS")[1]:
        
        # Mixer navigation (right)
        if ui.getFocused(0):
            ui.right()
        
        # General navigation
        else:
            ui.down()
    
    # 4D Encoder - to up (to improve navigation in general)
    if event.data1 == nihia.buttons.get("ENCODER_MINUS")[0] and event.data2 == nihia.buttons.get("ENCODER_MINUS")[1]:
        
        # Mixer navigation
        if ui.getFocused(0):
            ui.left()

        # General navigation
        else:
            ui.up()
    
    # 4D Encoder up
    if event.data1 == nihia.buttons.get("ENCODER_UP")[0] and event.data2 == nihia.buttons.get("ENCODER_UP")[1]:
        ui.up()
    
    # 4D Encoder down 
    if event.data1 == nihia.buttons.get("ENCODER_DOWN")[0] and event.data2 == nihia.buttons.get("ENCODER_DOWN")[1]:
        ui.down()
    
    # 4D Encoder (using FPT because ui.left doesn't work on the playlist)
    if event.data1 == nihia.buttons.get("ENCODER_LEFT")[0] and event.data2 == nihia.buttons.get("ENCODER_LEFT")[1]:
        ui.left()
    
    # 4D Encoder (using FPT because ui.right doesn't work on the playlist)
    if event.data1 == nihia.buttons.get("ENCODER_RIGHT")[0] and event.data2 == nihia.buttons.get("ENCODER_RIGHT")[1]:
        ui.right()

    # 4D Encoder button
    if event.data1 == nihia.buttons.get("ENCODER_BUTTON"):
        ui.enter()

    # Knobs
    # Normal knobs - increase values
    if event.data1 == nihia.knobs.get("KNOB_1A") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(0, "VOLUME", "INCREASE", mixer.trackNumber())
    
    if event.data1 == nihia.knobs.get("KNOB_2A") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(1, "VOLUME", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_3A") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(2, "VOLUME", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_4A") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(3, "VOLUME", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_5A") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(4, "VOLUME", "INCREASE", mixer.trackNumber())
    
    if event.data1 == nihia.knobs.get("KNOB_6A") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(5, "VOLUME", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_7A") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(6, "VOLUME", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_8A") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(7, "VOLUME", "INCREASE", mixer.trackNumber())
    
    # Normal knobs - decrease values
    if event.data1 == nihia.knobs.get("KNOB_1A") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(0, "VOLUME", "DECREASE", mixer.trackNumber())
    
    if event.data1 == nihia.knobs.get("KNOB_2A") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(1, "VOLUME", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_3A") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(2, "VOLUME", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_4A") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(3, "VOLUME", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_5A") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(4, "VOLUME", "DECREASE", mixer.trackNumber())
    
    if event.data1 == nihia.knobs.get("KNOB_6A") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(5, "VOLUME", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_7A") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(6, "VOLUME", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_8A") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(7, "VOLUME", "DECREASE", mixer.trackNumber())


    
    # Shifted knobs - increase values
    if event.data1 == nihia.knobs.get("KNOB_1B") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(0, "PAN", "INCREASE", mixer.trackNumber())
    
    if event.data1 == nihia.knobs.get("KNOB_2B") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(1, "PAN", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_3B") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(2, "PAN", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_4B") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(3, "PAN", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_5B") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(4, "PAN", "INCREASE", mixer.trackNumber())
    
    if event.data1 == nihia.knobs.get("KNOB_6B") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(5, "PAN", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_7B") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(6, "PAN", "INCREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_8B") and event.data2 == nihia.knobs.get("INCREASE"):
        adjustMixer(7, "PAN", "INCREASE", mixer.trackNumber())
    
    # Shifted knobs - decrease values
    if event.data1 == nihia.knobs.get("KNOB_1B") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(0, "PAN", "DECREASE", mixer.trackNumber())
    
    if event.data1 == nihia.knobs.get("KNOB_2B") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(1, "PAN", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_3B") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(2, "PAN", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_4B") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(3, "PAN", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_5B") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(4, "PAN", "DECREASE", mixer.trackNumber())
    
    if event.data1 == nihia.knobs.get("KNOB_6B") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(5, "PAN", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_7B") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(6, "PAN", "DECREASE", mixer.trackNumber())

    if event.data1 == nihia.knobs.get("KNOB_8B") and event.data2 == nihia.knobs.get("DECREASE"):
        adjustMixer(7, "PAN", "DECREASE", mixer.trackNumber())


######################################################################################################################
# Script logic
######################################################################################################################

def OnInit():

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

def OnIdle():
    # Updates the LED of the CLEAR button (moved to OnIdle, since OnRefresh isn't called when focused window changes)
    if ui.getFocused(midi.widPianoRoll) == True:
        nihia.buttonSetLight("CLEAR", 1)
    
    if ui.getFocused(midi.widPianoRoll) == False:
        nihia.buttonSetLight("CLEAR", 0)

    # Update peak meters
    # TODO: Disabled due to performance issues (multi-threading support needed)
    # ----------------------------------------------
    # updateMixerTracks("PEAK", mixer.trackNumber())
    # print("Peak updated.")
    # ----------------------------------------------


    


# Updates the LEDs and the mixer
def OnRefresh(HW_Dirty_LEDs):
    # PLAY button
    if transport.isPlaying() == True:
        nihia.buttonSetLight("PLAY", 1)
    
    if transport.isPlaying() == False:
        nihia.buttonSetLight("PLAY", 0)
    
    # STOP button
    if transport.isPlaying() == True:
        nihia.buttonSetLight("STOP", 0)
    
    if transport.isPlaying() == False:
        nihia.buttonSetLight("STOP", 1)
    
    # REC button
    if transport.isRecording() == True:
        nihia.buttonSetLight("REC", 1)
    
    if transport.isRecording() == False:
        nihia.buttonSetLight("REC", 0)

    # COUNT-IN button
    if ui.isPrecountEnabled() == True:
        nihia.buttonSetLight("COUNT_IN", 1)

    if ui.isPrecountEnabled() == False:
        nihia.buttonSetLight("COUNT_IN", 0)
    
    # CLEAR button (moved to OnIdle, since OnRefresh isn't called when focused window changes)

    # LOOP button
    if ui.isLoopRecEnabled() == True:
        nihia.buttonSetLight("LOOP", 1)
    
    if ui.isLoopRecEnabled() == False:
        nihia.buttonSetLight("LOOP", 0)

    # METRO button
    if ui.isMetronomeEnabled() == True:
        nihia.buttonSetLight("METRO", 1)

    if ui.isMetronomeEnabled() == False:
        nihia.buttonSetLight("METRO", 0)

    # MUTE button
    if mixer.isTrackMuted(mixer.trackNumber()) == True:
        nihia.buttonSetLight("MUTE", 1)

    if mixer.isTrackMuted(mixer.trackNumber()) == False:
        nihia.buttonSetLight("MUTE", 0)
    
    # SOLO button
    if mixer.isTrackSolo(mixer.trackNumber()) == True:
        nihia.buttonSetLight("SOLO", 1)

    if mixer.isTrackSolo(mixer.trackNumber()) == False:
        nihia.buttonSetLight("SOLO", 0)
    
    
    
def OnRefresh(HW_Dirty_Mixer_Sel):
    updateMixer()
    print("Mixer updated.")
