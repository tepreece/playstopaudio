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

import math, os

# Generic audio classes. All of the audio classes inherit from these, which
# implement placeholder methods for everything, and helper methods for parts
# that are just maths rather than involving the audio itself.

# An 'Audio' is a class that defines how this type of audio is going to work.
# It specifies which Sound class will be created, and optionally handles
# anything that needs to be done once - eg for Audiere, it handles the
# soundcard object.
class Audio():
	def __init__(self):
		self.sound_class = Sound
	
	def open_file(self, fname):
		# Open a file, and return a Sound for it.
		abs_fname = os.path.abspath(fname)
		return self.sound_class(self, abs_fname)

# A 'Sound' is a clip that is going to be played. The generic Sound class
# implements several helper methods, and the general get/set logic; the
# individual classes deal with actually playing out that audio.
class Sound():
	def __init__(self, fname):
		# time_const - usually (but not necessarily) the sample rate
		self.time_const = float(1)
	
	# 'length' and 'position' are in seconds; 'long_length' and 'long_position'
	# are in samples. The individual classes should generally just implement
	# long_length and long_position, and let the wrapper deal with the
	# conversion. Note that 'duration' is a synonym for length. NB - the
	# position is settable, but not the length (as that is determined by the
	# actual length of the clip that we loaded).
	def get_long_length(self):
		return 0
	
	def get_length(self):
		return self.long_length / self.time_const
		
	def get_long_position(self):
		return 0
	
	def get_position(self):
		return self.long_position / self.time_const
	
	def set_long_position(self, position):
		pass
	
	def set_position(self, position):
		self.long_position = position * self.time_const
	
	# 'volume' is generally on a scale of 0.0 - 1.0 (although this isn't
	# enforced, as you may want to go above that if the underlying audio
	# architecture supports it)
	def get_volume(self):
		return 0
	
	def set_volume(self, volume):
		pass
	
	# 'gain' is logarithmic; convert it to a volume so that it can be passed
	# to the audio architecture
	def get_gain(self):
		return 20*math.log10(self.volume)
	
	def set_gain(self, gain):
		self.volume = math.pow(10, float(gain)/20.0)
	
	# is the audio currently playing?
	def get_playing(self):
		return False
	
	# play, stop and pause the audio
	def play(self):
		pass
	
	def stop(self):
		pass
	
	def pause(self):
		pass
	
	# convert the above methods into properties on this object
	def __getattr__(self, name):
		if name == 'long_length' or name == 'long_duration':
			return self.get_long_length()
		elif name == 'length' or name == 'duration':			
			return self.get_length()
		elif name == 'long_position':
			return self.get_long_position()
		elif name == 'position':
			return self.get_position()
		elif name == 'volume':
			return self.get_volume()
		elif name == 'gain':
			return self.get_gain()
		elif name == 'playing':
			return self.get_playing()
	
	def __setattr__(self, name, val):
		if name == 'long_position':
			self.set_long_position(val)
		elif name == 'position':
			self.set_position(val)
		elif name == 'volume':
			self.set_volume(val)
		elif name == 'gain':
			return self.set_gain(val)
		else:
			self.__dict__[name]=val
	





