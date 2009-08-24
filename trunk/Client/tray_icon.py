import pygtk
pygtk.require('2.0')
import gtk

import cons

class TrayIcon(gtk.StatusIcon):
	""""""
	def __init__(self, show, hide, menu):
		""""""
		gtk.StatusIcon.__init__(self)
		self.set_tooltip(cons.PROGRAM_NAME + "- version " + cons.PROGRAM_VERSION)
		self.set_from_file(cons.ICON_PROGRAM)
		self.set_visible(True)

		self.window_visible = True
		self.show_window = show
		self.hide_window = hide

		self.menu = gtk.Menu()
		for item in menu:
			if item == None:
				tmp = gtk.SeparatorMenuItem()
			else:
				tmp = gtk.ImageMenuItem(item[0])
				tmp.connect('activate', item[1])
			self.menu.append(tmp)
		self.menu.show_all()

		self.connect('activate', self.activate)
		self.connect('popup-menu', self.popup_menu)

	def activate(self, statusicon, event=None):
		""""""
		if self.window_visible:
			self.hide_window()
			self.window_visible = False
		else:
			self.show_window()
			self.window_visible = True

	def popup_menu(self, statusicon, button, time):
		""""""
		self.menu.popup(None, None, gtk.status_icon_position_menu, button, time, self)

	def change_tooltip(self, statusbar, context, text):
		""""""
		#if context == "Downloads":
		tmp = text.split("\t")
		message = "Downloads: " + "".join(tmp[1:]) + "\n" + tmp[0].strip()
		self.set_tooltip(message)
