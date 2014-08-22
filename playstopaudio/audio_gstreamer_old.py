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

import gst, pygst

# Most of the documentation for what the different parameters mean and how to
# practically use them is found in the audio_generic module - you should
# probably read that instead unless you are particularly interested in the
# underlying workings of the GStreamer backend.

import audio_generic

# We don't actually need to do anything specific to get GStreamer going,
# but we need a basic Audio class to make it interchangeable with the other
# types.
class Audio_GStreamer_old(audio_generic.Audio):
	def __init__(self):
		self.sound_class = Sound_GStreamer

class Sound_GStreamer_old(audio_generic.Sound):
	def __init__(self, audio, fname):
		# not the sample rate, but what GStreamer uses...
		self.time_const = float(1000000000)
		
		# using a 'playbin2' player - much easier than setting up a full
		# pipeline, and sufficient for our purposes
		self.player = gst.element_factory_make("playbin2", "player")
		self.player.set_property("uri", "file://" + fname)
		
		# a bit of magic to get it to read the length properly
		# not really sure why this is needed...
		self.player.set_state(gst.STATE_PAUSED)
		if self.player.get_state()[1] == gst.STATE_PAUSED:
			throwaway = self.length
		self.player.set_state(gst.STATE_NULL)
		
		# GStreamer won't seek while the file isn't playing.
		# Work around this by storing a position so seek to immediately
		# upon starting to play.
		self._seek_to = None
	
	def get_long_length(self):
		# read the length if it isn't already cached
		# if something goes wrong (which it shouldn't), return zero
		if self._length is None:
			try:
				self._length = self.player.query_duration(gst.FORMAT_TIME, None)[0]
			except:
				self._length = 0
		return self._length
	
	def get_long_position(self):
		# if something goes wrong (which it shouldn't), return zero
		try:
			return self.player.query_position(gst.FORMAT_TIME, None)[0]
		except:
			return 0
	
	def set_long_position(self, position):
		if self.playing:
			# if playing, we can just seek
			self.player.seek_simple(
				gst.FORMAT_TIME,
				gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT, 
				position)
		else:
			# if not playing, set the position to seek to when we start playing
			self._seek_to = position
	
	def get_volume(self):
		return self.player.get_property('volume')
	
	def set_volume(self, volume):
		self.player.set_property('volume', volume)
	
	def get_playing(self):
		# get the playing state, and update our understanding of it if we've
		# played past the end (and are now stopped)
		if self.player.get_state()[1] == gst.STATE_PLAYING:
			if self.long_position >= self.long_duration:
				self.stop()
				return False
			return True
		return False
	
	def play(self):
		self.player.set_state(gst.STATE_PLAYING)
		# seek if needed
		if self._seek_to is not None:
			self.long_position = self._seek_to
			self._seek_to = None			
	
	def stop(self):
		self.player.set_state(gst.STATE_NULL)
	
	def pause(self):
		self.player.set_state(gst.STATE_PAUSED)





