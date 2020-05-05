# MIT License

# Copyright (c) 2020 Hobyst

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


# Library for using the NIHIA protocol on FL Studio's MIDI Scripting API

# This script contains all the functions and methods needed to take advantage of the deep integration
# features on Native Instruments' devices
# Any device with this kind of features will make use of this script

import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist

import midi
import utils


# Button name to button ID dictionary
# The button ID is the number in hex that is used as the DATA1 parameter when a MIDI message related to that button is
# sent or recieved from the device
buttons = {
    "PLAY": 0x10,
    "RESTART": 0x11,
    "REC": 0x12,
    "COUNT_IN": 0x13,
    "STOP": 0x14,
    "CLEAR": 0x15,
    "LOOP": 0x16,
    "METRO": 0x17,
    "TEMPO": 0x18,
    
    "UNDO": 0x20,
    "REDO": 0x21,
    "QUANTIZE": 0x22,
    "AUTO": 0x23,

    "MUTE": 0x43,
    "SOLO": 0x44,

    # Only on Maschine MK3, Maschine Studio and S-Series MK2 (TODO: NOT TESTED)
    "DPAD_X": 0x32,
    "DPAD_Y": 0x30
}


# Method to make talking to the device less annoying
# All the messages the device is expecting have a structure of "BF XX XX"
# The STATUS byte always stays the same and only the DATA1 and DATA2 vary
def dataOut(data1, data2):
    """ Function for easing the communication with the device. By just entering the DATA1 and DATA2 bytes of the MIDI message that has to be sent to the device, it 
    composes the full message in order to satisfy the syntax required by the midiOutSysex method, 
    as well as setting the STATUS of the message to BF as expected and sends the message. 
    
    data1, data2 -- Corresponding bytes of the MIDI message in hex format."""
    
    # Composes the MIDI message and sends it
    device.midiOutSysex(bytes([0xF0, 0xBF, data1, data2, 0xF7]))


# dataOut method but using int values
# DOESN'T WORK
# def dataOutInt(data1, data2):
    #     """ Variant of the dataOut method, but instead of having to use hex values you input int values
    #     and these get automatically converted to hex, the message is composed and then sent to the device. 
    
    #     data1, data2 -- Corresponding bytes of the MIDI message in integer format."""

    #     # Converts the values from int to hex format

    #     # Composes the MIDI message and sends it
    #     # device.midiOutSysex(bytes([0xF0, 0xBF, hex(data1), hex(data2), 0x14, 0x0C, 1, 0xF7]))


# Method to enable the deep integration features on the device
def handShake():
    """ Acknowledges the device that a compatible host has been launched, wakes it up from MIDI mode and activates the deep
    integration features of the device. TODO: Then waits for the answer of the device in order to confirm if the handshake 
    was successful and returns True if affirmative."""

    # Sends the MIDI message that initiates the handshake: BF 01 01
    dataOut(0x01, 0x01)

    # TODO: Waits and reads the handshake confirmation message

    

# Method to deactivate the deep integration mode. Intended to be executed on close.
def goodBye():
    """ Sends the goodbye message to the device and exits it from deep integration mode. 
    Intended to be executed before FL Studio closes."""

    # Sends the goodbye message: BF 02 01
    dataOut(0x02, 0x01)


# Method for restarting the protocol on demand. Intended to be used by the end user in case the keyboard behaves 
# unexpectedly.
def restartProtocol():
    """ Sends the goodbye message to then send the handshake message again. """

    # Turns off the deep integration mode
    goodBye()

    # Then activates it again
    handShake()

    
# Method for controlling the lighting on the buttons (for those who have idle/highlighted two state lights)
# Examples of this kind of buttons are the PLAY or REC buttons, where the PLAY button alternates between low and high light and so on.
# SHIFT buttons are also included in this range of buttons, but instead of low/high light they alternate between on/off light states.
def buttonSetLight(buttonName, lightMode):
    """ Method for controlling the lights on the buttons of the device. 
    
    buttonName -- Name of the button as shown in the device in caps and enclosed in quotes. ("PLAY", "AUTO", "REDO"...)

    EXCEPTION: declare the Count-In button as COUNT_IN
    
    lightMode -- If set to 0, sets the first light mode of the button. If set to 1, sets the second light mode."""

    #Light mode integer to light mode hex dictionary
    lightModes = {
        0: 0x00,
        1: 0x01
    }

    # Then sends the MIDI message using dataOut
    dataOut(buttons.get(buttonName, ""), lightModes.get(lightMode, ""))


mixerinfo_types = {
    "VOLUME": 0x50,
    "PAN": 0x58,
    "IS_MUTED": 0x43,
    "IS_SOLOED": 0x44,
    "NAME": 0x48,


}

# Method for reporting information about the mixer tracks
# TODO
def mixerInfo(info_type, value, trackID):
    """ Sends info about the mixer tracks to the device.
    
    info_type -- The kind of information you're going to send. ("VOLUME", "PAN"...)
    
    value -- Can be 0x00 or 0x01. Used for two-state properties like to tell if the track is solo-ed or not.
    
    trackID -- From 0x00 to 0x07. Tells the device which track from the ones that are showing up in the mixer you're going to tell info about."""

    device.midiOutSysex(bytes([0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, mixerinfo_types.get(info_type, 0x00), value, trackID]))

def mixerInfo2(info_type, value, trackID, additional_info):
    """ Sends info about the mixer tracks to the device.
    
    info_type -- The kind of information you're going to send. ("VOLUME", "PAN"...)
    
    value -- Can be 0x00 or 0x01. Used for two-state properties like to tell if the track is solo-ed or not.
    
    trackID -- From 0x00 to 0x07. Tells the device which track from the ones that are showing up in the mixer you're going to tell info about.
    
    additional_info -- Used for track name, track pan and track volume.
    """

