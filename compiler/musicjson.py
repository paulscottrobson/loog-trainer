# ******************************************************************************************
# ******************************************************************************************
#
#										Music JSON
#
# ******************************************************************************************
# ******************************************************************************************

from exception import CompilerException

class MusicJSON:
	#
	#	Constructor.
	#
	def __init__(self):
		self.bars = []
		self.settings = { "title":"","tempo":"100","tuning":"g3b3e4","beats":"4" }
	#
	#	Overwrite a setting.
	#
	def set(self,key,value):
		key = key.lower().strip()
		if key not in self.settings:
			raise CompilerException("Setting {0} unknown".format(key))
		# At present, one tuning.
		if key == "tuning":
			raise CompilerException("Changing tuning from g3b3e4 is not yet available")
		self.settings[key] = value.lower().strip()
	#
	#	Add a new bar.
	#
	def addBar(self):
		self.bars.append([])
		self.qbPosition = 0
	#
	#	Add a strum.
	#
	def addStrum(self,strum,qbLength):
		strum.append(qbLength)
		strum = "".join([chr(x+97) for x in strum])
		strum = strum[:-1]+strum[-1].upper()
		self.bars[-1].append(strum)
		self.qbPosition += qbLength
		if self.qbPosition > int(self.settings["beats"] * 4):
			raise CompilerException("Bar overflow")
		print(strum)
	#
	#	Render as JSON string
	#
	def render(self):
		render = "{\n"+"\n".join(['"{0}":"{1}",'.format(x,self.settings[x]) for x in self.settings.keys()])
		render = render+'\n"bars":[\n'
		render = render + "\n".join(['    "'+self.renderBar(x)+'",' for x in self.bars])
		return render+"\n]\n}"		
	#
	#	Render a bar
	#
	def renderBar(self,contents):
		return ";".join(contents)

if __name__ == '__main__':
	c = MusicJSON()
	for n in range(0,4):
		print("-------------	")
		c.addBar()
		for s in range(0,4+n):
			c.addStrum([n,s+1,s],2)
	print(c.render())		
