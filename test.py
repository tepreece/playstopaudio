#!/usr/bin/python

# Copyright (c) 2013 Thomas Preece
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from playstopaudio import playstopaudio
import sys, time

print 'Going to try playing the test file. Press ^C to quit.'

# Firstly, open an audio player. You can specify which types you are willing
# to accept - currently only 'gstreamer' and 'audiere'.

audio = playstopaudio.audio(['gstreamer', 'audiere'])

# Check that we've received a usable audio object.
if audio is None:
	sys.exit(1)

# Open an audio file. It can be a relative or absolute path.
af = audio.open_file('test.ogg')

# Set a start position (in seconds) and gain (in dB, ie it should be negative).
af.position = 0.0
af.gain = -0.0

# Start the file playing
af.play()
a = False

while True:
	# print some stats
	print af.duration, af.gain, af.position, af.playing
	
	# start it going when it stops
	if af.playing == False: af.play()
	
	# wait a second
	time.sleep(1)


