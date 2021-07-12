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

"""
FL Studio MIDI settings check module.
"""

import device

# midi_device_name = [deviceID, user_friendly_name]
supportedDevices = {
    # S-Series MK2
    "Komplete Kontrol DAW - 1": [0, "Komplete Kontrol S-Series MK2"],
    "Komplete Kontrol A DAW": [1, "Komplete Kontrol A-Series"],
    "Komplete Kontrol M DAW": [1, "Komplete Kontrol M32"]
}

wrongDevices = {
    "Komplete Kontrol S-Series MK2": ["KOMPLETE KONTROL - 1", "KOMPLETE KONTROL EXT - 1"],
    "Komplete Kontrol A-Series": ["KOMPLETE KONTROL A25 MIDI", "KOMPLETE KONTROL A49 MIDI", "KOMPLETE KONTROL A61 MIDI"],
    "Komplete Kontrol M32": "KOMPLETE KONTROL M32 MIDI"
}

#############################################################################################
# Errors
#############################################################################################

class DeviceNotValid(Exception):
    """ Raised when a non-supported device is found. """
    
    def __init__(self):
        print("The device the script is currently running over is not a Komplete Kontrol keyboard, and hence the script is not compatible with it.")
    
class WrongDevice(Exception):
    """ Raised when a supported device is detected, but the device the script is running over is not the DAW control device. """
    
    def __init__(self):
        print("A Komplete Kontrol keyboard has been detected, but the script isn't running over the DAW control port.")
        print("Please set this device named ", device.getName(), """ as a (generic controller) on the MIDI settings menu and assign it instead to 
        the device named """, supportedDevices.index(wrongDevices.index(device.getName())), ".")


#############################################################################################

def settingsCheck():
    """ Function that checks the FL Studio MIDI configuration the script is being launched with. """
    
    # Device name check against supportedDevices
    if (supportedDevices.get(device.getName(), -1) == -1):
        
        # Device name check against wrongDevices
        if wrongDevices.index(device.getName()) == ValueError:  # Devices not belonging to the Komplete Kontrol series
            raise DeviceNotValid(device.getName())
        
        else:                                                   # Devices belonging to the Komplete Kontrol series but setup is wrong
            raise WrongDevice()
    else:
        return supportedDevices.get(device.getName())[0]

