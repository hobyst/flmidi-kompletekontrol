# MIT License

# Copyright (c) 2021 Pablo Peral

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

import utils
import mixer
import plugins
import channels
import math
import midi
import ui

import config
import nihia.mixer

class Track:
    def __init__(self, id: int):
        # Physical ID of the track, from 0 to 7
        self.id = id

        # Equivalent of track index for the represented mixer track
        self.index = None

        # Existence and/or track type of the track
        self.exist = False

        # String to be displayed as the name of the track
        self.name = None
        
        # Number to be displayed as the volume of the track
        self.vol = None

        # Number to be displayed as the panning of the track
        self.pan = None

        # Armed for recording state
        self.armed = None

        # Selection state
        self.selected = None

        # Solo state
        self.solo = None

        # Mute state
        self.muted = None

    def update(self, trackFirst):
        # Disable track if it doesn't exist

        # Update track on the device if it exists
        # Index
        self.index = trackFirst + self.id

        # Existence is updated by the parent object `mixer_obj`

        # Name
        if mixer.getTrackName(self.index) != self.name:
            self.name = mixer.getTrackName(self.index)                          # Update cache
            nihia.mixer.setTrackName(self.id, mixer.getTrackName(self.index))   # Update device
        
        # Volume and volume graph
        if mixer.getTrackVolume(self.index) != self.vol:
            self.vol = mixer.getTrackVolume(self.index)
            nihia.mixer.setTrackVol(self.id, str(VolTodB(mixer.getTrackVolume(self.index))) + " dB")
            nihia.mixer.setTrackVolGraph(self.id, mixer.getTrackVolume(self.index))

        # Pan and pan graph
        if mixer.getTrackPan(self.index) != self.pan:
            self.pan = mixer.getTrackPan(self.index)
            
            # Centered
            if mixer.getTrackPan(self.index) == 0:
                nihia.mixer.setTrackPan(self.id, "Centered")
            
            # Right
            elif mixer.getTrackPan(self.index) > 0:
                nihia.mixer.setTrackPan(self.id, str(round((abs(mixer.getTrackPan(self.index)) * 100))) + "% " + "Right")

            # Left
            elif mixer.getTrackPan(self.index) < 0:
                nihia.mixer.setTrackPan(self.id, str(round((abs(mixer.getTrackPan(self.index)) * 100))) + "% " + "Left")

            nihia.mixer.setTrackPanGraph(self.id, mixer.getTrackPan(self.index))
        
        # Armed for recording state
        if mixer.isTrackArmed(self.index) != self.armed:
            self.armed = mixer.isTrackArmed
            nihia.mixer.setTrackArm(self.id, mixer.isTrackArmed(self.index))
        
        # Selection state
        if mixer.isTrackSelected(self.index) != self.selected:
            self.selected = mixer.isTrackSelected(self.index)
            nihia.mixer.setTrackSel(self.id, mixer.isTrackSelected(self.index))

        # Solo state
        if mixer.isTrackSolo(self.index) != self.solo:
            self.solo = mixer.isTrackSolo(self.index)
            nihia.mixer.setTrackSolo(self.id, mixer.isTrackSolo(self.index))
        
        # Mute state
        if mixer.isTrackMuted(self.index) != self.muted:
            self.muted = mixer.isTrackMuted(self.index)
            nihia.mixer.setTrackMute(self.id, mixer.isTrackMuted(self.index))

    def clear(self):
        self.__init__(self.id)

        nihia.mixer.setTrackExist(self.id, 0)
        nihia.mixer.setTrackName(self.id, "")
        nihia.mixer.setTrackVol(self.id, " ")
        nihia.mixer.setTrackVolGraph(self.id, 0)
        nihia.mixer.setTrackPan(self.id, " ")
        nihia.mixer.setTrackPanGraph(self.id, 0)
        nihia.mixer.setTrackArm(self.id, 0)
        nihia.mixer.setTrackSel(self.id, 0)
        nihia.mixer.setTrackSolo(self.id, 0)
        nihia.mixer.setTrackMute(self.id, 0)
        nihia.mixer.setTrackKompleteInstance(self.id, "")

class Mixer:
    def __init__(self):
        # The mixer section, in groups of 8, that is being currently displayed on the device
        self.trackGroup = None

        # The first track of the group
        self.trackFirst = None

        # Amount of tracks being shown in the display
        self.trackLimit = 8

        # Initialise mixer tracks on loop and store them in tracks list 
        self.tracks = []
        self.tracks += [Track(x) for x in range(8)]

        # List of tracks that need to be updated
        self.need_refresh = []

        # Variable to interface with OnDirtyMixerTrack with index -1
        self.need_full_refresh = False

        # Komplete Kontrol instance ID currently selected
        self.kompleteInstance = None

        # Mute and solo status for the currently selected track (for MUTE and SOLO buttons LEDs)
        self.isCurrentTrackMuted = None
        self.isCurrentTrackSolo = None

        # Peak meter values in 0-127 range
        self.previousPeakValues = []

    def whichTrackGroup(self, track: int) -> int:
        """ Function that calculates which track group has to be shown on screen by dividing 
        the mixer in groups of 8. 
        ### Arguments 
         - track (int): The mixer track you want to calculate the mixer group for.

        ### Returns
          - The calculated track group, from 0 to 15.
        """

        # Calculates which track group the current track belongs to and truncates the value to get the exact number
        trackGroup = math.trunc(1/8 * track)

        return trackGroup

    def update(self):
        # Schedules all tracks to be updated if trackGroup changes
        if (self.need_full_refresh == True):

            # Checks for the 15th group exception to limit track processing
            if self.trackGroup == 15:
                self.need_refresh = [0, 1, 2, 3, 4, 5]
            else:
                self.need_refresh = [0, 1, 2, 3, 4, 5, 6, 7]

        # Schedules all tracks to be updated if trackGroup changes
        if (self.whichTrackGroup(mixer.trackNumber()) != self.trackGroup):
            
            self.trackGroup = self.whichTrackGroup(mixer.trackNumber())
            self.trackFirst = self.trackGroup * 8

            # Also checks for the 15th group exception
            if self.trackGroup == 15:
                # Update track existence
                for x in range(6):
                    self.tracks[x].exist = 1
                self.tracks[6].clear()
                self.tracks[7].clear()
                
                for x in range(len(self.tracks)):
                    nihia.mixer.setTrackExist(self.tracks[x].id, self.tracks[x].exist)

                # Limit track processing
                self.need_refresh = [0, 1, 2, 3, 4, 5]
                self.trackLimit = 6
            else:
                # Update track existence
                for x in range(len(self.tracks)):
                    self.tracks[x].exist = 1

                for x in range(len(self.tracks)):
                    nihia.mixer.setTrackExist(self.tracks[x].id, self.tracks[x].exist)

                # Limit track processing
                self.need_refresh = [0, 1, 2, 3, 4, 5, 6, 7]
                self.trackLimit = 8

            # Updates FL Studio mixer rectangle halo
            ui.miDisplayRect(self.trackFirst, self.trackFirst + self.trackLimit - 1, midi.MaxInt)

        # Updates mute and solo status of the currently selected track (for MUTE and SOLO button lights)
        if mixer.isTrackMuted(mixer.trackNumber()) != self.isCurrentTrackMuted:
            self.isCurrentTrackMuted = mixer.isTrackMuted(mixer.trackNumber())
            nihia.mixer.setCurrentTrackMuted(mixer.isTrackMuted(mixer.trackNumber()))
        
        if mixer.isTrackSolo(mixer.trackNumber()) != self.isCurrentTrackSolo:
            self.isCurrentTrackSolo = mixer.isTrackSolo(mixer.trackNumber())
            nihia.mixer.setCurrentTrackSolo(mixer.isTrackSolo(mixer.trackNumber()))

        # Updates scheduled tracks
        for x in range(len(self.need_refresh)):
            self.tracks[self.need_refresh[x]].update(self.trackFirst)
        
        # Resets update queue
        self.need_refresh = []

        # Checks Komplete Kontrol instance
        if plugins.isValid(channels.selectedChannel()) == True:                                   # Checks if plugin exists
            if plugins.getPluginName(channels.selectedChannel()) == "Komplete Kontrol":           # Checks if plugin is Komplete Kontrol
                if self.kompleteInstance != plugins.getParamName(0, channels.selectedChannel()):  # Checks against cache and updates if necessary
                    self.kompleteInstance = plugins.getParamName(0, channels.selectedChannel())
                    nihia.mixer.setTrackKompleteInstance(0, plugins.getParamName(0, channels.selectedChannel()))
            
            else:
                if self.kompleteInstance != "":  # Checks against cache and updates if necessary
                    self.kompleteInstance = ""
                    nihia.mixer.setTrackKompleteInstance(0, "")

        else:
            if self.kompleteInstance != "":  # Checks against cache and updates if necessary
                self.kompleteInstance = ""
                nihia.mixer.setTrackKompleteInstance(0, "")

    def sendPeakInfo(self):
        """ Method to serially update peak meter values shown on the screen of S-Series MK2 devices. 
        """

        # Creates peakList if peak values are going to be updated
        peakList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Gets the 16 peak values that need to be reported to the device by building a list [peakL_0, peakR_0, peakL_1, peakR_1 ...]
        for x in range(self.trackFirst, self.trackFirst + self.trackLimit):
            peakList[(x - self.trackFirst) * 2] = mixer.getTrackPeaks(x, midi.PEAK_L)
            peakList[(x - self.trackFirst) * 2 + 1] = mixer.getTrackPeaks(x, midi.PEAK_R)

        # Performs 0-1.1 to 0-127 range conversion to make cache more conscious about actual changes regarding
        # the information that the device actually utilizes
        for x in range(0, 16):
            # Makes the max of the peak meter on the device match the one on FL Studio (values that FL Studio gives seem to be infinite)
            if peakList[x] > 1.1:
                peakList[x] = 1.1
        
            # Translates the 0-1.1 range to 0-127 range
            peakList[x] = peakList[x] * (127 / 1.1)
        
            # Truncates the possible decimals and declares the number as an integer to avoid errors in the translation of the data
            peakList[x] = int(math.trunc(peakList[x]))

        if peakList != self.previousPeakValues:
            # Updates peak values on the cache
            self.previousPeakValues = peakList

            # Updates peak values on the device
            nihia.mixer.sendPeakMeterData(peakList)

def VolTodB(value: float):

    if value == 0:
        dB = "-oo"
        str(dB)
    else:
        dB = (math.exp(value * 1.25 * math.log(11)) - 1) * 0.1
        dB = round(math.log10(dB) * 20, 1)

    return dB
