# Copyright (c) 2013 - 2014 Thomas Preece
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

class PlayStopAudioException(Exception):
	pass

# General constructor method to create the correct sort of audio class - the
# interesting parts are in the classes themselves.
def audio(classlist=('gstreamer', 'gstreamer_old', 'audiere')):
	for c in classlist:
		if c == 'gstreamer':
			try:
				import audio_gstreamer
				return audio_gstreamer.Audio_GStreamer()
			except:
				pass
		elif c == 'gstreamer_old':
			try:
				import audio_gstreamer_old
				return audio_gstreamer.Audio_GStreamer_old()
			except:
				pass
		elif c == 'audiere':
			try:
				import audio_audiere
				return audio_audiere.Audio_Audiere()
			except:
				pass
		else:
			raise PlayStopAudioException('Unknown audio class: %s' % c)
	raise PlayStopAudioException('No usable audio classes.')
	return None
	
