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

# Imports Native Instruments Host Integration Agent library
import nihia.core

# Defines button IDs
PLAY =     10
RESTART =  11
REC =      12
COUNT_IN = 13
STOP =     14
CLEAR =    15
LOOP =     16
METRO =    17
TEMPO =    18
UNDO =     20
REDO =     21
QUANTIZE = 22
AUTO =     23
MASTER =   43
SOLO =     44

# These are for the dot-lights found in the 4D Encoder of S-Series and certain Maschine devices.
# It should not make any effect on devices without these dot-lights.
# IT HASN'T BEEN TESTED IF THIS WORKS OR NOT

# Lights can't be set one by one because the DATA1 byte is the same for both buttons that control the same axis
# It has to be done by axis
DPAD_X = 32
DPAD_Y = 30

def OnInit():
    # Makes the handshake with NIHIA
    nihia.core.handShake()

    # Prints a little help message
    print("If you run into issues, run nihia.core.restartProtocol() to fix device freezing.")