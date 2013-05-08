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

import audiere
import audio_generic

class Audio_Audiere(audio_generic.Audio):
	def __init__(self):
		self.sound_class = Sound_Audiere
		self.audiere = audiere.open_device()

class Sound_Audiere(audio_generic.Sound):
	def __init__(self, audio, fname):
		self.time_const = float(44100)
		self.audiere = audio.audiere
		self.audiofile = self.audiere.open_file(fname, True)
	
	def get_long_length(self):
		return self.audiofile.length
	
	def get_long_position(self):
		return self.audiofile.position
	
	def get_playing(self):
		return bool(self.audiofile.playing)
	
	def play(self):
		self.audiofile.play()
	
	def stop(self):
		self.audiofile.stop()
	
	def pause(self):
		self.audiofile.pause()





