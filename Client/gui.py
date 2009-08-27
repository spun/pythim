#! /usr/bin/env python
import sys
import pygtk
if not sys.platform == 'win32':
        pygtk.require('2.0')
import gtk
import os
import gobject
import socket

import webbrowser

from about import About
from tray_icon import TrayIcon
from menu_bar import MenuBar
from libNotify import notification

import cons

class Gui():
	""""""

			
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_icon_from_file(cons.ICON_PROGRAM)
		self.window.set_resizable(True)
		self.window.connect("destroy", self.close_application)
		self.window.set_title(cons.PROGRAM_NAME)
		
		vboxAdm = gtk.VBox()
		self.window.add(vboxAdm)
		vboxAdm.show()
				
		# Menu items
		menu_quit = gtk.STOCK_QUIT, self.close_application
		menu_help = gtk.STOCK_HELP, self.help
		menu_about = gtk.STOCK_ABOUT, About
		menu_preferences = gtk.STOCK_PREFERENCES, self.close_application
		show_conex = gtk.CheckMenuItem("Conexiones"), True,  self.hideshowConexionEntry, self.hideshowConexionEntry


		# Menubar
		file_menu = ("Archivo"), [menu_quit]
		view_menu = ("Ver"), [show_conex, None, menu_preferences]
		help_menu = ("Ayuda"), [menu_help, menu_about]
		vboxAdm.pack_start(MenuBar([file_menu, view_menu, help_menu]), False)
		vboxAdm.show()	
		
		self.window.set_size_request(600, 400)
		self.vbox1 = gtk.VBox()
		vboxAdm.pack_start(self.vbox1, True, True, 0)
		self.vbox1.show()
		self.vbox1.set_border_width(10)	
		
		self.hbox1 = gtk.HBox()
		self.vbox1.pack_end(self.hbox1, True, True, 10)
		self.hbox1.show()
		
		self.makeChatArea()
		self.makeConexionEntry()
		self.makeUsersOnline()
		
		# Barra de estado (completamente innecesaria)
		self.statusbar = gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("Users")
		vboxAdm.pack_end(self.statusbar, False, False, 0)
		self.statusbar.show()
		
		
		self.window.show()
		
		
	def conect_socket(self, widget, host, port, user):
		
		info_conex= "Se intentara conectar a "+ host+":"+ str(port)+ " como \"" + user.get_text() + "\""
		
		self.textbuffer.set_text(info_conex)
		try:
			self.s = socket.socket()
			self.s.connect(("localhost", 9999))
			nick=user.get_text()
			self.s.send(nick)
			gobject.idle_add(self.recv_text)
			start_text="\nConectado\n\n"
			color = "green"
			
		except:
			start_text="\nNo se pudo conectar\n\n"
			color = "red"
			
		final = self.textbuffer.get_end_iter()
		startiter =  self.textbuffer.get_end_iter().get_offset()

		self.textbuffer.insert(self.textbuffer.get_iter_at_offset(startiter), start_text)
		startiter = self.textbuffer.get_iter_at_offset(startiter)
		enditer = self.textbuffer.get_end_iter()
		
		tag = self.textbuffer.create_tag(None, foreground = color)
		self.textbuffer.apply_tag(tag, startiter, enditer)
		
	def recv_text(self):
		try:
			mensaje=self.s.recv(1024)
			self.s.settimeout(.1)
			final = self.textbuffer.get_end_iter()
			self.textbuffer.insert(final,mensaje)
			# scroll al final al recibir
			self.textview.scroll_to_mark(self.textbuffer.get_insert(), 0)
			return True
		except:
			return True		
		
	def send_text(self, widget):
		inicio = self.textbuffer2.get_start_iter()
		final = self.textbuffer2.get_end_iter()
		entry_text = self.textbuffer2.get_text(inicio, final)
		
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
		elif entry_text == "@salir":
			self.quit()
			
		# Hacemos el salto de linea		
		entry_text = str(entry_text) + "\n"
		
		# Insertamos texto al final del textbox
		final = self.textbuffer.get_end_iter()
		self.textbuffer.insert(final, os.environ["USERNAME"] + " dice:\n")
		self.textbuffer.insert(final,entry_text)
		# scroll al final al escribir
		self.textview.scroll_to_mark(self.textbuffer.get_insert(), 0)

		
		# Vaciamos la caja de entrada de texto
		self.textbuffer2.set_text("")	
		
	def makeChatArea(self):
		
		vpaned = gtk.VPaned()
		vpaned.SetPosition=550
		self.hbox1.pack_start(vpaned, True, True, 0)
		vpaned.show()		
		sw = gtk.ScrolledWindow()
		sw.set_size_request(0, 230)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		sw.set_shadow_type(gtk.SHADOW_IN)
		self.textview = gtk.TextView()
		self.textview.set_editable(False)
		self.textview.set_wrap_mode(gtk.WRAP_WORD)
		self.textbuffer = self.textview.get_buffer()
		sw.add(self.textview)
		sw.show()
		self.textview.show()
		vpaned.add1(sw)
		
		hbox = gtk.HBox()
		vpaned.add2(hbox)
		
		hbox.show()		
		hbox.set_size_request(0, 500)
		sw2 = gtk.ScrolledWindow()
		sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw2.set_shadow_type(gtk.SHADOW_IN)
		textview2 = gtk.TextView()
		textview2.set_wrap_mode(gtk.WRAP_WORD)
		self.textbuffer2 = textview2.get_buffer()
		sw2.add(textview2)
		sw2.show()
		textview2.show()
		hbox.pack_start(sw2, True, True, 0)
		
		button = gtk.Button("Enviar")
		button.connect("clicked", self.send_text)
		button.show()
		hbox.pack_start(button, False, False, 0)

	
	
	def statusConexionEntry(self, widget):
		if self.show_conect:
			return True
		else:
			return False

	# Oculta o muestra la barra de conexiones
	def hideshowConexionEntry(self, widget):
		if self.show_conect:
			self.hboxConex.hide()
			self.show_conect=False
			print "a"
		else:
			self.hboxConex.show()
			self.show_conect=True
			print "b"
			
	def makeConexionEntry(self):
		
		self.hboxConex = gtk.HBox()
		self.vbox1.pack_start(self.hboxConex, False, False, 0)
		self.hboxConex.show()
		self.show_conect = True

			
		hostText =gtk.Entry()
		hostText.set_text("localhost")
		self.hboxConex.pack_start(hostText, True, True, 0)
		hostText.show()
		
		portText = gtk.Entry()
		portText.set_text("9999")
		self.hboxConex.pack_start(portText, True, True, 0)
		portText.show()
		
		aliasText = gtk.Entry()
		
		try:
			name = os.environ["USERNAME"]
		except:
			name = "Anonimo"

		aliasText.set_text(name)
		self.hboxConex.pack_start(aliasText, True, True, 0)
		aliasText.show()

		button = gtk.Button("Conectar")
		button.connect("clicked", self.conect_socket, hostText.get_text(), int(portText.get_text()), aliasText)
		self.hboxConex.pack_start(button, True, True, 0)
		button.show()


	# Oculta o muestra la barra de conexiones
	def hideshowUsersOnline(self, widget, response=None):
		if self.show_UsersOnline:
			self.scrolled_window.hide()
			self.show_UsersOnline=False
		else:
			self.scrolled_window.show()
			self.show_UsersOnline=True
			
	def makeUsersOnline(self):
		
		self.vboxUsers = gtk.VBox()
		self.hbox1.pack_end(self.vboxUsers, False, False, 0)
		self.vboxUsers.show()
		
		
        # Create a new scrolled window, with scrollbars only if needed
		self.scrolled_window = gtk.ScrolledWindow()
		self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		model = gtk.ListStore(gobject.TYPE_STRING)
		tree_view = gtk.TreeView(model)
		#tree_view.connect("button_press_event", lambda x,y: scrolled_window.hide())
		self.scrolled_window.add_with_viewport (tree_view)
		tree_view.show()
		#scrolled_window.show()
		self.show_UsersOnline = False

        # Add some messages to the window
		for i in range(10):
			msg = "Usuario #%d" % i
			iter = model.append()
			model.set(iter, 0, msg)

		cell = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Usuarios conectados", cell, text=0)
		tree_view.append_column(column)
		
		self.vboxUsers.pack_start(self.scrolled_window, True, True, 0)

		
		
		button = gtk.Button()
		self.vboxUsers.pack_end(button, False, False, 0)
		arrow = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_ETCHED_OUT)
		button.add(arrow)
		button.connect("button_press_event", self.hideshowUsersOnline)
		button.set_size_request(15, 15)
		button.show()
		arrow.show()
		
		return self.scrolled_window


	# Abre el navegador en la web de documentacion
	def help(self, widget):
		""""""
		webbrowser.open(cons.DOC)
		
	def close_application(self, dialog=None, response=None):
		try:
			self.s.send("@salir")
			self.s.close()			
			gtk.main_quit()
		except:
			gtk.main_quit()

def main():
	gtk.main()

if __name__ == "__main__":
	g = Gui()
	main()
