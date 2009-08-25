#! /usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os

import socket

import webbrowser

from about import About
from tray_icon import TrayIcon
from menu_bar import MenuBar
from libNotify import notification

import cons

class Gui(gtk.Window):
	""""""
	def __init__(self):

		menu_quit = gtk.STOCK_QUIT, self.quit
		menu_about = gtk.STOCK_ABOUT, About	
		
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_size_request(600, 400)
		self.set_icon_from_file(cons.ICON_PROGRAM)
		self.set_title(cons.PROGRAM_NAME)
		#self.move(self.x, self.y)
		
		self.connect("delete_event", self.quit)
		
		
		# socket cliente
		try:
			self.s = socket.socket()
			self.s.connect(("localhost", 9999))
			start_text="Conectado\n\n"
		except:
			start_text="No se pudo conectar\n\n"
		
		
		# Caja de ventana (sin borde)
		vboxAdm = gtk.VBox()
		self.add(vboxAdm)
		vboxAdm.show()
		
		
		# Menu items
		menu_quit = gtk.STOCK_QUIT, self.quit
		menu_help = gtk.STOCK_HELP, self.help
		menu_about = gtk.STOCK_ABOUT, About
		menu_preferences = gtk.STOCK_PREFERENCES, self.quit

		# Menubar
		file_menu = ("Archivo"), [menu_quit]
		view_menu = ("Editar"), [menu_preferences]
		help_menu = ("Ayuda"), [menu_help, menu_about]
		vboxAdm.pack_start(MenuBar([file_menu, view_menu, help_menu]), False)
		vboxAdm.show()		
		
		
		# Caja de elementos (con borde)
		vbox = gtk.VBox()
		vboxAdm.pack_start(vbox, True, True, 0)
		vbox.show()
		vbox.set_border_width(10)	
		
		
		# Textview box
		sw = gtk.ScrolledWindow()
		vbox.pack_start(sw, True, True, 0)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		sw.set_shadow_type(gtk.SHADOW_IN)
		textview = gtk.TextView()
		textview.set_editable(False)
		textview.set_border_width(2)
		self.textbuffer = textview.get_buffer()
		sw.add(textview)
		sw.show()
		textview.show()
		# Informamos si se pudo conectar o no
		self.textbuffer.set_text(start_text)		
		
		
		# Label de separacion
		label = gtk.Label("Escribir mensaje:")
		label.set_justify(gtk.JUSTIFY_LEFT)
		vbox.pack_start(label, False, False, 0)
		label.show()
		
		
		# Caja de elementos (con borde)
		hbox = gtk.HBox()
		vbox.pack_start(hbox, False, False, 0)
		hbox.show()
		
		# Entry box
		entry = gtk.Entry()
		entry.set_max_length(50)
		entry.connect("activate", self.send_text, entry)
		entry.set_text("Tu texto")
		entry.insert_text(" aqui", len(entry.get_text()))
		entry.select_region(0, len(entry.get_text()))
		hbox.pack_start(entry, True, True, 0)
		entry.show()
		
		# Boton de conectar
		button = gtk.Button("Enviar")
		button.connect("clicked", self.send_text, entry)
		hbox.pack_start(button, False, False, 0)
		button.show()
		
		
		
		# Barra de estado (completamente innecesaria)
		self.statusbar = gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("Users")
		vboxAdm.pack_end(self.statusbar, False, False, 0)
		self.statusbar.show()
		
		
		# Muestra la ventana
		self.show()
		
		
		# Trayicon
		tray_menu = [menu_about, None, menu_quit]
		self.tray_icon = TrayIcon(self.show, self.hide, tray_menu)
		
		
	def send_text(self, widget, entry):
		entry_text = entry.get_text()
		
		# Informacion al terminal
		print "Contenido caja: %s\n" % entry_text
		
		# Mandamos el mensaje al servidor
		try:
			self.s.send(entry_text)
		except:
			print "No se pudo enviar el mensaje"
		
		# Primera version de notificaciones
		if entry_text == "beta":
			g = notification()
			g.notify()
			
		# Hacemos el salto de linea		
		entry_text = entry_text + "\n"
		
		# Insertamos texto al final del textbox
		final = self.textbuffer.get_end_iter()
		self.textbuffer.insert(final, os.environ["USERNAME"] + " dice:\n")
		self.textbuffer.insert(final,entry_text)
		
		# Vaciamos la caja de entrada de texto
		entry.set_text("")	


	# Abre el navegador en la web de documentacion
	def help(self, widget):
		""""""
		webbrowser.open(cons.DOC)


	# Cierre de aplicacion
	def quit(self, dialog=None, response=None):
		""""""
		try:
			self.s.close()
			gtk.main_quit()
		except:
			gtk.main_quit()
		return False


def main():
	gtk.main()

if __name__ == "__main__":
	g = Gui()
	main()
