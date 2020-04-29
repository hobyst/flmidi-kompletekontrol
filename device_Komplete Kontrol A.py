# name=Native Instruments Komplete Kontrol A-Series
# url = 

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


# Function to make talking to the keyboard less annoying
# All the messages the keyboard is expecting have a structure of "BF XX XX"
# The STATUS byte stays always the same and only the DATA1 and DATA2 vary

def KompleteDataOut(data1, data2):
    """ Function for easing the communication with the keyboard. By just entering the DATA1 and DATA2 bytes of the MIDI message that has to be sent to the keyboard, it 
    composes the full message in order to satisfy the syntax required by Python's midiOut functions, 
    as well as setting the STATUS of the message to BF as expected. """
    device.midiOutSysex(bytes([0xF0, 0xBF, data1, data2, 0x14, 0x0C, 1, 0xF7]))

def OnInit():
    # Makes the handshake with NIHIA
    KompleteDataOut(0x01, 0x01)
