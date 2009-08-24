# -*- coding: utf-8 -*-

import gtk
import cons

try:
	import pynotify
	if not pynotify.init("pyim"):
		raise
except:
	print "there was a problem initializing the pynotify module"
	


class notification:
	""""""
	def __init__(self):

		pynotify.init("pyim")
  
	def notify(self, title="Hola usuario", text="Estas viendo una caracteristica aun en prueba"):
		notification = pynotify.Notification(title, text)
		p = gtk.gdk.pixbuf_new_from_file(cons.ICON_PROGRAM)
		notification.set_icon_from_pixbuf(p)
		notification.show()
