# ******************************************************************************************
# ******************************************************************************************
#
#										Chord Library
#
# ******************************************************************************************
# ******************************************************************************************

class ChordLibrary:
	#
	#	Constructor
	#
	def __init__(self):
		# This looks up chord names to fingerings.
		self.chords = {}
		# Get the raw data.
		src = ChordLibrary.RAWDATA.lower().replace("\t"," ").replace("\n"," ").split(" ")
		for c in [x for x in src if x != ""]:
			# Work out name and fingering.
			chordName = c.split(":")[0]
			chordFingering = [int(x) for x in c.split(":")[1]]
			# Put in library
			self.chords[chordName] = chordFingering 
			#print(chordName,chordFingering)
			# can we 'sharp' it - A# C# D# F# G# only !
			if chordName[0] != 'b' and chordName[0] != 'e':
				chordName = chordName[0]+"#"+chordName[1:]
				chordFingering = [x+1 for x in chordFingering]				
				# Put in library
				self.chords[chordName] = chordFingering 
				#print(chordName,chordFingering)
				# Convert to flat.
				cNote = chordName[0]
				cNote = chr(ord(cNote)+1) if cNote != 'g' else 'a'
				chordName = cNote+"b"+chordName[2:]
				# Put in library
				self.chords[chordName] = chordFingering 
				#print(chordName,chordFingering)
	#
	#	Locate a chord, return None if not present
	#
	def find(self,chord):
		chord = chord.lower().strip()
		return self.chords[chord] if chord in self.chords else None


ChordLibrary.RAWDATA = """

A:220 B:442 C:010 D:232 E:100 F:211 G:003 
Am:210 Bm:432 Cm:543 Dm:231 Em:000 Fm:111 Gm:333

"""

if __name__ == '__main__':
	c = ChordLibrary()
	print(c.chords)
