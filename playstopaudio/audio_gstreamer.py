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


# The way to import GStreamer has changed. Fortunately the code is the same
# in either case - just the import method changes. Try both ways.

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
	

# Most of the documentation for what the different parameters mean and how to
# practically use them is found in the audio_generic module - you should
# probably read that instead unless you are particularly interested in the
# underlying workings of the GStreamer backend.

import audio_generic

class Audio_GStreamer(audio_generic.Audio):
	def __init__(self):
		Gst.init(None)
		self.sound_class = Sound_GStreamer

class Sound_GStreamer(audio_generic.Sound):
	def __init__(self, audio, fname):
		# not the sample rate, but what GStreamer uses...
		self.time_const = float(1000000000)
		
		# using a 'playbin2' player - much easier than setting up a full
		# pipeline, and sufficient for our purposes
		self.player = Gst.ElementFactory.make("playbin", "player")
		self.player.set_property("uri", "file://" + fname)
		
		# a bit of magic to get it to read the length properly
		# not really sure why this is needed...
		self.player.set_state(Gst.State.PAUSED)
		throwaway = self.length
		self.player.set_state(Gst.State.NULL)
		
		# GStreamer won't seek while the file isn't playing.
		# Work around this by storing a position so seek to immediately
		# upon starting to play.
		self._seek_to = None
	
	def get_long_length(self):
		# read the length if it isn't already cached
		# if something goes wrong (which it shouldn't), return zero
		return self.player.query_duration(Gst.Format.TIME)[1]
	
	def get_long_position(self):
		# if something goes wrong (which it shouldn't), return zero
		#try:
			return self.player.query_position(Gst.Format.TIME)[1]
		#except:
		#	return 0
	
	def set_long_position(self, position):
		if self.playing:
			# if playing, we can just seek
			self.player.seek_simple(
				Gst.Format.TIME,
				Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 
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
		if self.player.get_state(0)[1] == Gst.State.PLAYING:
			if self.long_position >= self.long_duration:
				self.stop()
				return False
			return True
		return False
	
	def play(self):
		self.player.set_state(Gst.State.PLAYING)
		# seek if needed
		if self._seek_to is not None:
			self.long_position = self._seek_to
			self._seek_to = None			
	
	def stop(self):
		self.player.set_state(Gst.State.NULL)
	
	def pause(self):
		self.player.set_state(Gst.State.PAUSED)





