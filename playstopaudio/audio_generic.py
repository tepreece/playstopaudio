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

class Audio():
	def __init__(self):
		self.sound_class = Sound
	
	def open_file(self, fname):
		abs_fname = os.path.abspath(fname)
		return self.sound_class(self, abs_fname)

class Sound():
	def __init__(self, fname):
		self.time_const = float(1)
	
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
	
	def get_volume(self):
		return 0
	
	def set_volume(self, volume):
		pass
	
	def get_gain(self):
		return 20*math.log10(self.volume)
	
	def set_gain(self, gain):
		self.volume = math.pow(10, float(gain)/20.0)
		print self.volume
	
	def get_playing(self):
		return False
	
	def play(self):
		pass
	
	def stop(self):
		pass
	
	def pause(self):
		pass
	
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
	





