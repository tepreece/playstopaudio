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

import pygst
import gst

import audio_generic

class Audio_GStreamer(audio_generic.Audio):
	def __init__(self):
		self.sound_class = Sound_GStreamer

class Sound_GStreamer(audio_generic.Sound):
	def __init__(self, fname):
		self.time_const = float(1000000000)
		self.player = gst.element_factory_make("playbin2", "player")
		self.player.set_property("uri", "file://" + fname)
		
		# a bit of magic to get it to read the length properly
		# not really sure why this is needed...
		self.player.set_state(gst.STATE_PAUSED)
		if self.player.get_state()[1] == gst.STATE_PAUSED:
			throwaway = self.length
		self.player.set_state(gst.STATE_NULL)
	
	def get_long_length(self):
		if self._length is None:
			try:
				self._length = self.player.query_duration(gst.FORMAT_TIME, None)[0]
			except:
				self._length = 0
		return self._length
	
	def get_long_position(self):
		try:
			return self.player.query_position(gst.FORMAT_TIME, None)[0]
		except:
			return 0
	
	def get_playing(self):
		if self.player.get_state()[1] == gst.STATE_PLAYING:
			if self.long_position >= self.long_duration:
				self.stop()
				return False
			return True
		return False
	
	def play(self):
		self.player.set_state(gst.STATE_PLAYING)
	
	def stop(self):
		self.player.set_state(gst.STATE_NULL)
	
	def pause(self):
		self.player.set_state(gst.STATE_PAUSED)





