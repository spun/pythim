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

	def __init__(self):

		menu_quit = gtk.STOCK_QUIT, self.quit
		menu_about = gtk.STOCK_ABOUT, About	
		
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_size_request(300, 500)
		self.set_icon_from_file(cons.ICON_PROGRAM)
		self.set_title(cons.PROGRAM_NAME)
		
		#self.move(self.x, self.y)
		
		self.connect("delete_event", self.delete_event)
		self.vbox = gtk.VBox()
		self.add(self.vbox)
				
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
		
		self.show_all()
		
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
