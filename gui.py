#! /usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

import webbrowser

from about import About
from tray_icon import TrayIcon

from menu_bar import MenuBar

import cons

class Gui(gtk.Window):
	""""""
	# Our new improved callback.  The data passed to this method
	# is printed to stdout.
	def callback(self, widget, data):
		print "Hello again - %s was pressed" % data

	# another callback
	def delete_event(self, widget, event, data=None):
		gtk.main_quit()
		return gtk.FALSE

	def muestra_texto(self, widget, entry):
		entry_text = entry.get_text()
		print "Contenido caja: %s\n" % entry_text
		
	def menuitem_response(self, widget, string):
		print "%s" % string
		
	def __init__(self):

		menu_quit = gtk.STOCK_QUIT, self.quit
		menu_about = gtk.STOCK_ABOUT, About	
		
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_size_request(600, 400)
		self.set_icon_from_file(cons.ICON_PROGRAM)
		self.set_title(cons.PROGRAM_NAME)
		
		#self.move(self.x, self.y)
		
		self.connect("delete_event", self.delete_event)
		
		self.vbox = gtk.VBox()
		self.add(self.vbox)
		self.vbox.show()	
		
		#menu items
		menu_quit = gtk.STOCK_QUIT, self.quit
		menu_help = gtk.STOCK_HELP, self.help
		menu_about = gtk.STOCK_ABOUT, About
		menu_preferences = gtk.STOCK_PREFERENCES, self.quit

		#menubar
		file_menu = ("Archivo"), [menu_quit]
		view_menu = ("Editar"), [menu_preferences]
		help_menu = ("Ayuda"), [menu_help, menu_about]
		self.vbox.pack_start(MenuBar([file_menu, view_menu, help_menu]), False)
		self.vbox.show()		
		

		#entry box
		entry = gtk.Entry()
		entry.set_max_length(50)
		entry.connect("activate", self.muestra_texto, entry)
		entry.set_text("hello")
		entry.insert_text(" world", len(entry.get_text()))
		entry.select_region(0, len(entry.get_text()))
		self.vbox.pack_end(entry, gtk.TRUE, gtk.TRUE, 0)
		entry.show()

		self.show()
		
		#trayicon
		tray_menu = [menu_about, None, menu_quit]
		self.tray_icon = TrayIcon(self.show, self.hide, tray_menu)
		
		
	def help(self, widget):
		""""""
		webbrowser.open(cons.DOC)
		
	def quit(self, dialog=None, response=None):
		""""""
		gtk.main_quit()
		return gtk.FALSE

def main():
	gtk.main()

if __name__ == "__main__":
	g = Gui()
	main()
