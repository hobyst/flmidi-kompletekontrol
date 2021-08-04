# MIT License

# Copyright (c) 2021 Hobyst

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import mixer_definition
import nihia
from nihia import *
import config

import mixer
import transport
import general
import ui
import device
import midi
import plugins
import channels
import math

class Core:
    """ Common controller definition across all Komplete Kontrol keyboards. """
    def __init__(self):
        # Initialize mixer cache
        self.mixer = mixer_definition.Mixer()

        # Variable for the window change produced by the Quantize button
        self.window = -1

        # Variable for the window change produced by the Quantize button (second implementation)
        self.window2 = 63

    def OnInit(self):
        # Activates the deep integration mode
        nihia.handShake()

        # Sets the lights on
        nihia.buttons.setLight("PLAY", 0)
        nihia.buttons.setLight("REC", 0)
        nihia.buttons.setLight("COUNT_IN", 0)
        nihia.buttons.setLight("STOP", 0)
        nihia.buttons.setLight("CLEAR", 1)
        nihia.buttons.setLight("LOOP", 0)
        nihia.buttons.setLight("METRO", 0)
        nihia.buttons.setLight("UNDO", 1)
        nihia.buttons.setLight("REDO", 1)
        nihia.buttons.setLight("QUANTIZE", 1)
        nihia.buttons.setLight("REDO", 1)
        nihia.buttons.setLight("TEMPO", 1)

        # Additional controller-dependent code
        try:
            self.OnInitAdd()
        except:
            pass

        # Update mixer
        self.mixer.update()

    def OnInitAdd(self):                # Intended to be declared by child
        raise NotImplementedError()

    def OnDeInit(self):
        # Deactivates the deep integration mode
        nihia.goodBye()

    def OnMidiMsg(self, event):
        # Play button
        if event.data1 == nihia.buttons.button_list.get("PLAY"):
            event.handled = True
            transport.start()

        # Restart button
        elif event.data1 == nihia.buttons.button_list.get("RESTART"):
            event.handled = True
            transport.setLoopMode()

        # Record button
        elif event.data1 == nihia.buttons.button_list.get("REC"):
            event.handled = True
            transport.record()
        
        # Count-In button
        elif event.data1 == nihia.buttons.button_list.get("COUNT_IN"):
            event.handled = True
            
            # Defines the standard behavior (just to toggle "Countdown before recording" on/off)
            if config.COUNT_IN_BEHAVIOR == 0:
                transport.globalTransport(midi.FPT_CountDown, 1)
            
            # Defines behavior of the button if the user chooses the Maschine-alike behavior
            if config.COUNT_IN_BEHAVIOR == 1:
        
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
        elif event.data1 == nihia.buttons.button_list.get("STOP"):
            event.handled = True
            transport.stop()

        # Clear button
        # This one in other DAWs (in Maschine, specifically) this button is meant to clear the MIDI clip you're
        # on so you can record again on it without having to use a mouse to delete all of the notes on the clip before
        # recording again
        #
        # However, since the MIDI API on FL Studio doesn't allow control over the piano roll specifically, for now it will only just
        # emulate the delete button (which does the same)
        elif event.data1 == nihia.buttons.button_list.get("CLEAR"):
            event.handled = True
            ui.delete()
        
        # Loop button (toggles loop recording on/off)
        elif event.data1 == nihia.buttons.button_list.get("LOOP"):
            event.handled = True
            transport.globalTransport(midi.FPT_LoopRecord, 1)

        # Metronome button
        elif event.data1 == nihia.buttons.button_list.get("METRO"):
            event.handled = True
            transport.globalTransport(midi.FPT_Metronome, 1)
        
        # Tempo button
        elif event.data1 == nihia.buttons.button_list.get("TEMPO"):
            event.handled = True
            transport.globalTransport(midi.FPT_TapTempo, 1)


        # Undo button
        elif event.data1 == nihia.buttons.button_list.get("UNDO"):
            event.handled = True
            general.undoUp()
        
        # Redo button
        elif event.data1 == nihia.buttons.button_list.get("REDO"):
            event.handled = True
            general.undo()

        
        # Quantize button
        # TODO: Not implemented yet in FL Studio MIDI API
        # 
        # Instead, it changes between FL windows
        # TODO: The code is correctly written, but the ui.showWindow() method has a bug that causes the Piano roll and Browser windows not to
        # appear when invoked. It has been said it should be fixed in a future update.
        # -----------------------------------------------------------------------------------------------------------------------------------
        # if event.data1 == nihia.buttons.button_list.get("QUANTIZE"):
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
        elif event.data1 == nihia.buttons.button_list.get("QUANTIZE"):
            event.handled = True
            self.window2 += 1

            # Normal behavior if the action ID is between the desired range
            if self.window2 <= 68 and self.window2 != 67:
                transport.globalTransport(self.window2, 1)
            
            # Skips the 67 value which calls the full screen plugin picker and calls the mixer instead
            elif self.window2 == 67:
                self.window2 += 1
                transport.globalTransport(self.window2, 1)

            # Once window value is out of range, it sets it again to the first value in range
            elif self.window2 > 68:
                self.window2 = 64
                transport.globalTransport(self.window2, 1)


        # Automation button
        # Enables and disables the recording automation events
        # TODO: Not implemented yet in FL Studio MIDI API
        # 
        # Instead, it shows the full-screen plugin browser
        elif event.data1 == nihia.buttons.button_list.get("AUTO"):
            event.handled = True
            transport.globalTransport(midi.FPT_F8, 1)

        # 4D Encoder +
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL") and event.data2 == nihia.buttons.button_list.get("PLUS"):
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
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL") and event.data2 == nihia.buttons.button_list.get("MINUS"):
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
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_VOLUME_SELECTED") and event.data2 == nihia.buttons.button_list.get("PLUS"):
            event.handled = True
            mixer.setTrackVolume(mixer.trackNumber(), mixer.getTrackVolume(mixer.trackNumber()) + 0.01)
        
        # 4D Encoder - (selected track volume)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_VOLUME_SELECTED") and event.data2 == nihia.buttons.button_list.get("MINUS"):
            event.handled = True
            mixer.setTrackVolume(mixer.trackNumber(), mixer.getTrackVolume(mixer.trackNumber()) - 0.01)

        
        # 4D Encoder + (selected track pan)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_PAN_SELECTED") and event.data2 == nihia.buttons.button_list.get("PLUS"):
            event.handled = True
            mixer.setTrackPan(mixer.trackNumber(), mixer.getTrackPan(mixer.trackNumber()) + 0.01)
        
        # 4D Encoder + (selected track pan)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_PAN_SELECTED") and event.data2 == nihia.buttons.button_list.get("MINUS"):
            event.handled = True
            mixer.setTrackPan(mixer.trackNumber(), mixer.getTrackPan(mixer.trackNumber()) - 0.01)
        
        # 4D Encoder button
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON"):
            event.handled = True

            # Open and close plugin window for the currently selected plugin on the channel rack
            if ui.getFocused(midi.widChannelRack) == True:
                channels.showEditor(channels.channelNumber(), 1)
            elif ui.getFocused(5) == True:
                channels.showEditor(channels.channelNumber(), 0)
            else:
                ui.enter()
        
        # 4D Encoder button (shifted)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON_SHIFTED"):
            event.handled = True
            transport.globalTransport(midi.FPT_Menu, 1)

        # Knobs
        # Normal knobs (volume adjustment)

        elif nihia.mixer.knobs[0][0] <= event.data1 <= nihia.mixer.knobs[0][7]:
            event.handled = True
            # Increase
            if nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                self.adjustMixer(event.data1 - nihia.mixer.knobs[0][0], "VOLUME", "INCREASE", mixer.trackNumber())
            
            # Decrease
            elif nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                self.adjustMixer(event.data1 - nihia.mixer.knobs[0][0], "VOLUME", "DECREASE", mixer.trackNumber())
        
        # Shifted knobs (pan adjustment)
        elif nihia.mixer.knobs[1][0] <= event.data1 <= nihia.mixer.knobs[1][7]:
            event.handled = True
            # Increase
            if nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                self.adjustMixer(event.data1 - nihia.mixer.knobs[1][0], "PAN", "INCREASE", mixer.trackNumber())
            
            # Decrease
            elif nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                self.adjustMixer(event.data1 - nihia.mixer.knobs[1][0], "PAN", "DECREASE", mixer.trackNumber())
        
        # Additional controller-dependent code
        try:
            self.OnMidiMsgAdd(event)
        except:
            pass

    def OnMidiMsgAdd(self, event):      # Intended to be declared by child
        raise NotImplementedError()

    def OnIdle(self):
        # Updates the LED of the CLEAR button (moved to OnIdle, since OnRefresh isn't called when focused window changes)
        if ui.getFocused(midi.widPianoRoll) == True:
            nihia.buttons.setLight("CLEAR", 1)
        
        elif ui.getFocused(midi.widPianoRoll) == False:
            nihia.buttons.setLight("CLEAR", 0)

    def OnRefresh(self, flag):

        # LEDs update
        if flag == midi.HW_Dirty_LEDs:
            # PLAY button
            if transport.isPlaying() == True:
                nihia.buttons.setLight("PLAY", 1)
            
            elif transport.isPlaying() == False:
                nihia.buttons.setLight("PLAY", 0)
            
            # STOP button
            if transport.isPlaying() == True:
                nihia.buttons.setLight("STOP", 0)
            
            elif transport.isPlaying() == False:
                nihia.buttons.setLight("STOP", 1)
            
            # REC button
            if transport.isRecording() == True:
                nihia.buttons.setLight("REC", 1)
            
            elif transport.isRecording() == False:
                nihia.buttons.setLight("REC", 0)

            # COUNT-IN button
            if ui.isPrecountEnabled() == True:
                nihia.buttons.setLight("COUNT_IN", 1)

            elif ui.isPrecountEnabled() == False:
                nihia.buttons.setLight("COUNT_IN", 0)
            
            # CLEAR button (moved to OnIdle, since OnRefresh isn't called when focused window changes)

            # LOOP button
            if ui.isLoopRecEnabled() == True:
                nihia.buttons.setLight("LOOP", 1)
            
            elif ui.isLoopRecEnabled() == False:
                nihia.buttons.setLight("LOOP", 0)

            # METRO button
            if ui.isMetronomeEnabled() == True:
                nihia.buttons.setLight("METRO", 1)

            elif ui.isMetronomeEnabled() == False:
                nihia.buttons.setLight("METRO", 0)

            # MUTE button
            if mixer.isTrackMuted(mixer.trackNumber()) == True:
                nihia.buttons.setLight("MUTE_SELECTED", 1)

            elif mixer.isTrackMuted(mixer.trackNumber()) == False:
                nihia.buttons.setLight("MUTE_SELECTED", 0)
            
            # SOLO button
            if mixer.isTrackSolo(mixer.trackNumber()) == True:
                nihia.buttons.setLight("SOLO_SELECTED", 1)

            elif mixer.isTrackSolo(mixer.trackNumber()) == False:
                nihia.buttons.setLight("SOLO_SELECTED", 0)

        else:
            self.mixer.update()

    def OnDirtyMixerTrack(self, index):
        if index == -1:
            self.mixer.need_full_refresh = True

        # Queue an update for a specific track
        elif self.mixer.trackFirst <= index < self.mixer.trackFirst + self.mixer.trackLimit:
            self.mixer.need_refresh += [index - self.mixer.trackFirst]

    def OnUpdateMeters(self):           # Intended to be declared by child
        raise NotImplementedError()

    def adjustMixer(self, knob: int, dataType: str, action: str, selectedTrack: int):
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

        if (trackGroup == 15) and (knob == 6 or knob == 7): # Control 15th group exception
            return

        else:
            if dataType == "VOLUME":
                if action == "INCREASE":
                    mixer.setTrackVolume(trackFirst + knob, mixer.getTrackVolume(trackFirst + knob) + config.KNOB_INCREMENTS_VOL)
                
                elif action == "DECREASE":
                    mixer.setTrackVolume(trackFirst + knob, mixer.getTrackVolume(trackFirst + knob) - config.KNOB_INCREMENTS_VOL)

            elif dataType == "PAN":
                if action == "INCREASE":
                    mixer.setTrackPan(trackFirst + knob, mixer.getTrackPan(trackFirst + knob) + config.KNOB_INCREMENTS_PAN)

                elif action == "DECREASE":
                    mixer.setTrackPan(trackFirst + knob, mixer.getTrackPan(trackFirst + knob) - config.KNOB_INCREMENTS_PAN)

class A_Series(Core):
    """ Controller code specific to A/M-Series keyboards. """
    def OnMidiMsgAdd(self, event):
        # Mute button - A-Series
        if event.data1 == nihia.buttons.button_list.get("MUTE_SELECTED"):
            event.handled = True
            mixer.muteTrack(mixer.trackNumber())

        # Solo button - A-Series
        elif event.data1 == nihia.buttons.button_list.get("SOLO_SELECTED"):
            event.handled = True
            mixer.soloTrack(mixer.trackNumber())
        
        # 4D Encoder up
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A") and event.data2 == nihia.buttons.button_list.get("UP"):
            event.handled = True
            ui.up()

        # 4D Encoder down 
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A") and event.data2 == nihia.buttons.button_list.get("DOWN"):
            event.handled = True
            ui.down()

        # 4D Encoder (using FPT because ui.left doesn't work on the playlist)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_X_A") and event.data2 == nihia.buttons.button_list.get("LEFT"):
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
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_X_A") and event.data2 == nihia.buttons.button_list.get("RIGHT"):
            event.handled = True
            if ui.getFocused(midi.widMixer) == True:
                # This one doesn't move the mixer view as you get to the border
                # ----------------------------------------------------
                # mixer.setTrackNumber(mixer.trackNumber() + 1)
                # ----------------------------------------------------
                ui.right()
            
            else:
                ui.right()

class S_SeriesMK2(Core):
    """ Controller code specific to S-Series MK2 keyboards. """
    def OnInitAdd(self):
        # Tells to FL Studio the device has peak meters
        device.setHasMeters()

        # Sets the lights of the 4D Encoder on S-Series keyboards on
        nihia.buttons.setLight("ENCODER_X_S", 1)
        nihia.buttons.setLight("ENCODER_X_S", 127)
        nihia.buttons.setLight("ENCODER_Y_S", 1)
        nihia.buttons.setLight("ENCODER_Y_S", 127)

    def OnMidiMsgAdd(self, event):
        # Mute button - S-Series
        if event.data1 == nihia.buttons.button_list.get("MUTE"):
            event.handled = True
            self.mixerMuteSoloHandler("MUTE", event.data2, mixer.trackNumber())

        # Solo button - S-Series
        elif event.data1 == nihia.buttons.button_list.get("SOLO"):
            event.handled = True
            self.mixerMuteSoloHandler("SOLO", event.data2, mixer.trackNumber())
        
        # 4D Encoder up
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_Y_S") and event.data2 == nihia.buttons.button_list.get("UP"):
            event.handled = True
            ui.up()

        # 4D Encoder down 
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_Y_S") and event.data2 == nihia.buttons.button_list.get("DOWN"):
            event.handled = True
            ui.down()

        # 4D Encoder (using FPT because ui.left doesn't work on the playlist)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_X_S") and event.data2 == nihia.buttons.button_list.get("LEFT"):
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
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_X_S") and event.data2 == nihia.buttons.button_list.get("RIGHT"):
            event.handled = True
            if ui.getFocused(midi.widMixer) == True:
                # This one doesn't move the mixer view as you get to the border
                # ----------------------------------------------------
                # mixer.setTrackNumber(mixer.trackNumber() + 1)
                # ----------------------------------------------------
                ui.right()
            
            else:
                ui.right()

    def OnUpdateMeters(self):
        self.mixer.sendPeakInfo()

    def mixerMuteSoloHandler(self, action: str, targetTrack: int, selectedTrack: int):
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

        elif action == "SOLO":
            mixer.soloTrack(trackFirst + targetTrack)
