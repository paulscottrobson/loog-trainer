# ******************************************************************************************
# ******************************************************************************************
#
#									Compiler Superclass
#
# ******************************************************************************************
# ******************************************************************************************

from musicjson import MusicJSON
from exception import CompilerException
from compiler import Compiler
from chords import ChordLibrary

import re

class ChordCompiler(Compiler):
	#
	#	Initialise compiler
	#
	def compilerInitialise(self):
		self.strumPattern = "d-" * self.getBeats()
		self.lastChord = None
		self.library = ChordLibrary()
	#
	#	Compile the bar
	#
	def compileBar(self,barDef):
		# rip out pattern information
		m = re.search("\{(.*?)\}",barDef)
		while m is not None:
			self.strumPattern = m.group(1).strip().lower()
			if len(self.strumPattern) != self.getBeats()*2:
				raise CompilerException("Bad strum pattern "+self.strumPattern)
			barDef = barDef.replace(m.group(0),"")
			m = re.search("\{(.*?)\}",barDef)
			#print("Found",barDef,self.strumPattern)
		# rip out chord information
		chords = [ self.lastChord ] * self.getBeats()
		m = re.search("\[(.*?)\]",barDef)
		while m is not None:
			barDef = barDef.replace(m.group(0),"")
			# add :1 on end if not present
			newChord = m.group(1) if m.group(1).find(":") >= 0 else m.group(1)+":1"
			# if begins with :, e.g. it ends the chord, make it x:1
			newChord = newChord if newChord[0] != ':' else 'x'+newChord
			newChord = newChord.split(":")
			# fill up bar from start position with chord.
			for i in range(int(newChord[1])-1,self.getBeats()):
				chords[i] = newChord[0] if newChord[0] != 'x' else None
			#print(newChord)
			m = re.search("\[(.*?)\]",barDef)
		# remove double spacing
		while barDef.find("  ") >= 0:
			barDef = barDef.replace("  "," ").strip()
		# what's left is he lyric
		self.musicjson.setLyric(barDef)
		# print(">>",barDef,self.strumPattern,chords)
		# the next bar starts with the last chord of this bar.
		self.lastChord = chords[-1]
		# for each half beat, render the appropriate chord, or not :)
		for halfBeat in range(0,self.getBeats()*2):
			if self.strumPattern[halfBeat] != "-":
				chord = chords[int(halfBeat/2)]
				if chord is not None:
					cDef = self.library.find(chord)
					if cDef == None:
						raise CompilerException("Unknown chord "+chord)
					self.musicjson.addStrum(cDef,2)

if __name__ == '__main__':
	c = ChordCompiler("let-it-be.chords")
	c.write("../app/music.json")
	print(c.render())