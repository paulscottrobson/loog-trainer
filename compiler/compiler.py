# ******************************************************************************************
# ******************************************************************************************
#
#									Compiler Superclass
#
# ******************************************************************************************
# ******************************************************************************************

from musicjson import MusicJSON
from exception import CompilerException

class Compiler:
	#
	#	Constructor. Note one instance per compilation.
	#
	def __init__(self,sourceFile):
		self.musicjson = MusicJSON()
		self.sourceFile = sourceFile
		self.lineNumber = 0
		self.compilerInitialise()
		self.preProcess()	
		self.compile()
	#
	#	Called to set stuff up
	#
	def compilerInitialise(self):
		self.strumPattern = "d-" * self.getBeats()
	#
	#	Pre process comments, control chars 
	#
	def preProcess(self):
		# Preprocess file.
		self.src = [x.replace("\t"," ").lower() for x in open(self.sourceFile).readlines()]
		self.src = [x if x.find("//") < 0 else x[:x.find("//")] for x in self.src]
		self.src = [x.strip() for x in self.src]
	#
	#	Compile the body.
	#
	def compile(self):
		# Scan through file.
		for n in range(0,len(self.src)):
			self.lineNumber = n+1
			# process the a := b stuff
			if self.src[n].find(":=") >= 0:
				parts = [x.strip() for x in self.src[n].split(":=")]
				self.musicjson.set(parts[0],parts[1])
			else:
				parts = [x.strip() for x in self.src[n].split("|") if x.strip() != ""]
				for p in parts:
					self.musicjson.addBar()
					self.compileBar(p)
	#
	#	Compile the bar
	#
	def compileBar(self,barDef):
		print(barDef)
	#
	#	Render the result
	#
	def render(self):
		return self.musicjson.render()
	#
	#	Get number of beats
	#		
	def getBeats(self):
		return int(self.musicjson.get("beats"))
	#
	#	Write the render out
	#
	def write(self,targetFile):
		open(targetFile,"w").write(self.render())
if __name__ == '__main__':
	c = Compiler("let-it-be.chords")
	print(c.render())