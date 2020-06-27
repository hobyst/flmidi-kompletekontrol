# name=Native Instruments Komplete Kontrol A
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

# Imports time library
import time


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

# Tempo adjustment mode
tempo_adjust = 0
tempo_press_count= 0

# Declaration of the method that will keep FL redirecting input for tempo control as long as the user is adjusting the tempo
# TODO
def tempoMode(event):
    """ Triggers """
    
    global tempo_adjust
    global tempo_press_count
    
    while tempo_adjust == 1:
        
        # When the tempo button is pressed it enters the tempo adjustment mode
        if event.data1 == nihia.buttons.get("TEMPO") and tempo_press_count == 1:
            # When Encoder + is triggered, modifies the tempo by +1
            if event.data1 == nihia.buttons.get("ENCODER_PLUS")[0] and event.data2 == nihia.buttons.get("ENCODER_PLUS")[1]:
                transport.globalTransport(midi.FPT_TempoJog, 10)
        
            # When Encoder - is triggered, modifies the tempo by -1
            if event.data1 == nihia.buttons.get("ENCODER_MINUS")[0] and event.data2 == nihia.buttons.get("ENCODER_MINUS")[1]:
                transport.globalTransport(midi.FPT_TempoJog, -10)
        
            # When any other key or button is triggered, it is used for tempo tapping
            else:
                transport.globalTransport(midi.FPT_TapTempo, 1)

        # When the tempo button is pressed again it exits the tempo adjustment mode
        if event.data1 == nihia.buttons.get("TEMPO") and tempo_press_count == 2:
            tempo_adjust = 0


# Variable for the window change produced by the Quantize button
window = -1

# Variable for the window change produced by the Quantize button (second implementation)
window2 = 63

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
    # Enables tempo tapping on the keys/pads of the device and tempo jogging using the 4D encoder
    # TODO


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
    # TODO


    # Solo button
    # TODO


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


def OnDeInit():
    # Deactivates the deep integration mode
    nihia.goodBye()


def OnUpdateBeatIndicator(value):
    # Play button blinking -- code snippet based on one from soundwrightpro
    if transport.isPlaying() == True:
        # Make it turn on on beat change
        if value == 2:
            nihia.buttonSetLight("PLAY", 1)
        # Make it turn on on bar change
        elif value == 1:
            nihia.buttonSetLight("PLAY", 1)
        # Make it turn off when there is no change
        else:
            nihia.buttonSetLight("PLAY", 0)

# Updates the LEDs
def OnRefresh(HW_Dirty_LEDs):
    # Play button may get stuck on highlighted state when playback is paused
    if transport.isPlaying() == False:
        nihia.buttonSetLight("PLAY", 0)
    