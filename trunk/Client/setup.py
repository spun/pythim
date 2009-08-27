# setup.py
from distutils.core import setup
import py2exe
import glob

opts = {
    "py2exe": {
        "includes": "pango,atk,gobject,cairo,pangocairo",
        "dll_excludes": [
        "iconv.dll","intl.dll","libatk-1.0-0.dll",
        "libgdk_pixbuf-2.0-0.dll","libgdk-win32-2.0-0.dll",
        "libglib-2.0-0.dll","libgmodule-2.0-0.dll",
        "libgobject-2.0-0.dll","libgthread-2.0-0.dll",
        "libgtk-win32-2.0-0.dll","libpango-1.0-0.dll",
        "libpangowin32-1.0-0.dll"],
        }
    }

setup(
    name = "Pyim",
    description = "A nice GUI interface for those with GiantDisc jukebox systems.",
    version = "0.61",
    windows = [
        {"script": "pyim.py"}
    ],
    options=opts,
)
