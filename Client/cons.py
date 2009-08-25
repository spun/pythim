import sys
import os

# project constants
PROGRAM_NAME = "Pyim"
PROGRAM_VERSION = "0.0.5 alpha"
WEBPAGE = "http:///"
DOC = "http://www.google.es/"

#path constants
if "win" in sys.platform:
	PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
	DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "").decode(locale.getdefaultlocale()[1])
	if PATH not in sys.path:
		sys.path.insert(0, PATH)
else:
	PATH = os.path.join(sys.path[0], "")
	DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "")
CONFIG_PATH = os.path.join(DEFAULT_PATH, ".pyim" ,"")


#media constants
PATH_MEDIA = os.path.join(PATH, "media", "")
ICON_PROGRAM = PATH_MEDIA + "globe.png"

