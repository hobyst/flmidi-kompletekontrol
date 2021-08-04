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
User-editable Python file to change script behavior.
"""
# Any line of this file starting with hashes (#) is a comment and won't be interpreted by FL Studio

# Behavior of the Count-In button
# 
# If set to 0, it will toggle on/off the "Countdown before recording" option on FL Studio
# If set to 1, it will act like on the Maschine software: it will make FL Studio jump straight into record mode with 
# the "Countdown before recording" option enabled
COUNT_IN_BEHAVIOR = 0

# Knob increments
# These values set the amount of increments for each message your keyboard sends to FL Studio
# when twisting the knobs on your device to change track volume and pan on the mixer
# Defaults are:
# - KNOB_INCREMENTS_VOL = 0.02
# - KNOB_INCREMENTS_PAN = 0.02
KNOB_INCREMENTS_VOL = 0.02
KNOB_INCREMENTS_PAN = 0.02