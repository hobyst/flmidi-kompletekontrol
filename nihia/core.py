# Core library for using the NIHIA protocol

# This script contains all the functions and methods needed to take advantage of the deep integration
# features on Native Instruments' devices
# Any device with this kind of features will make use of this script

import fl
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


# Method to make talking to the device less annoying
# All the messages the device is expecting have a structure of "BF XX XX"
# The STATUS byte always stays the same and only the DATA1 and DATA2 vary
def dataOut(data1, data2):
    """ Function for easing the communication with the device. By just entering the DATA1 and DATA2 bytes of the MIDI message that has to be sent to the device, it 
    composes the full message in order to satisfy the syntax required by the midiOutSysex method, 
    as well as setting the STATUS of the message to BF as expected and sends the message. 
    
    data1, data2 -- Corresponding bytes of the MIDI message in hex format."""
    
    # Composes the MIDI message and sends it
    device.midiOutSysex(bytes([0xF0, 0xBF, data1, data2, 0x14, 0x0C, 1, 0xF7]))


# dataOut method but using int values
def dataOutInt(data1, data2):
    """ Variant of the dataOut method, but instead of having to use hex values you input int values
    and these get automatically converted to hex, the message is composed and then sent to the device. 
    
    data1, data2 -- Corresponding bytes of the MIDI message in integer format."""

    # Converts the values from int to hex format
    data1 = hex(data1)
    data2 = hex(data2)

    # Composes the MIDI message and sends it
    device.midiOutSysex(bytes([0xF0, 0xBF, data1, data2, 0x14, 0x0C, 1, 0xF7]))


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
def buttonLightSet(buttonName, lightMode):
    """ Method for controlling the lights on the buttons of the device. 
    
    buttonName -- Name of the button as shown in the device in caps. (PLAY, AUTO, REDO...)

    EXCEPTION: declare the Count-In button as COUNT_IN
    
    lightMode -- If set to 0, sets the first light mode of the button. If set to 1, sets the second light mode."""

    # Based on the buttonName, finds the right DATA1 parameter (integer-formated) for the MIDI message
    # In order to do this, rather than using an if statement I'm using a Python dictionary to emulate the logic of a switch-case statement
    buttons = {
        'PLAY':     10,
        'RESTART':  11,
        'REC':      12,
        'COUNT_IN': 13,
        'STOP':     14,
        'CLEAR':    15,
        'LOOP':     16,
        'METRO':    17,
        'TEMPO':    18,
        'UNDO':     20,
        'REDO':     21,
        'QUANTIZE': 22,
        'AUTO':     23,
        'MASTER':   43,
        'SOLO':     44,

        # These are for the dot-lights found in the 4D Encoder of S-Series and certain Maschine devices.
        # It should not make any effect on devices without these dot-lights.
        # IT HASN'T BEEN TESTED IF THIS WORKS OR NOT

        # Lights can't be set one by one because the DATA1 byte is the same for both buttons that control the same axis
         'DPAD_X': 32,
         'DPAD_Y': 30
    }
    
    # Gets the result from the button dictionary and assigns the button ID to a variable that will be then used to conform the message
    button = buttons.get(buttonName, 0)

    # Sends the MIDI message using dataOutInt
    dataOutInt(button, lightMode)
