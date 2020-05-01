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


def OnInit():
    # Makes the handshake with NIHIA
    nihia.core.handShake()
