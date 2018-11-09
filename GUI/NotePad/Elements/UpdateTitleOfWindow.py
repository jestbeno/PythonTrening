import os

def update_title(self):
	self.setWindowTitle("%s - Megasolid Idiom" % (os.path.basename(self.path) if self.path else "Untitled"))
