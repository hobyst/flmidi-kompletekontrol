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

# Quantize button behavior
# - If set to 0 (default), it will serve as a quantize buttom for the notes the currently selected pattern and currently
#   selected channel rack
# - If set to 1, it will behave the way it did before the implementation of quantization in the MIDI scripting API
#   and allow jumping between FL Studio windows
QUANTIZE_BEHAVIOR = 0

# Quantize mode (only matters if QUANTIZE_BEHAVIOR is set to 0)
# - If set to 0, quantization will be applied to both start and end time of notes
# - If set to 1 (default), quantization will be applied only to start time of notes
QUANTIZE_MODE = 1

# Mixer halo behavior 
# - If set to 0, nothing will appear over the current group of tracks
# - If set to 1 (default), a rectangle halo will appear over the current group of tracks
MIXER_HALO_BEHAVIOR = 1
