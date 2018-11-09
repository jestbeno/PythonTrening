#####################################################################
################## RENAMING FILES TO RIGHT FORMAT ###################
#####################################################################

# PRINTING ERRORS
# RENAMING FILES
# GET FILES FROM DIR, SUBDIR,...

import os

path_preimenovanjeMMTdatotek=r'C:\Users\nucic\Desktop\PYTHON\AutomateTheBoraringStuff\RenamingFiles_Subfiles'

def preimenovanjeMMTdatotek():
	for root, dirs, files in os.walk(path_preimenovanjeMMTdatotek):
		for name in files:
			try:
				if (name.endswith(".mmt") and len(name) > 19):
					os.rename(root + os.sep + name, root + os.sep + name[:15] + '.mmt')
			except Exception as e:
				print(e)
				print("Datoteka z imenom: " + name + ", že obstaja!")

preimenovanjeMMTdatotek()

