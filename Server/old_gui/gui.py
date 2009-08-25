#! /usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

import socket

import webbrowser

class Gui(gtk.Window):
	""""""		
	def __init__(self):
		
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_size_request(200, 300)
		#self.set_icon_from_file(cons.ICON_PROGRAM)
		self.set_title("servidor")
		
		self.connect("delete_event", self.quit)
		
		# Caja vertical
		vbox = gtk.VBox()
		self.add(vbox)
		vbox.show()	
		
		# Campo de entrada para la direccion
		label = gtk.Label("Direccion:")
		label.set_justify(gtk.JUSTIFY_LEFT)
		vbox.pack_start(label, False, False, 0)
		label.show()

		porttext = gtk.Entry()
		porttext.set_max_length(50)
		porttext.set_text("localhost")
		vbox.pack_start(porttext, False, False, 0)
		porttext.show()
		
		
		# Campo de entrada para el puerto
		label = gtk.Label("Puerto:")
		label.set_justify(gtk.JUSTIFY_LEFT)
		vbox.pack_start(label, False, False, 0)
		label.show()
		
		map = gtk.Entry()
		map.set_text("9999")
		vbox.pack_start(map, False, False, 0)
		map.show()
		
		
		# Boton de conectar
		button = gtk.Button("Conectar")
		button.connect("clicked", self.startService, porttext.get_text(), int(map.get_text()))
		vbox.pack_start(button, False, False, 0)
		button.show()
		
		
		# Barra de estado (completamente innecesaria)
		self.statusbar = gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("Users")
		vbox.pack_end(self.statusbar, False, False, 0)
		self.statusbar.show()
		
		
		# Campo de texto de informacion (para cuando se realice una conexion...)
		sw =gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		sw.set_shadow_type(gtk.SHADOW_IN)
		textview = gtk.TextView()
		textview.set_editable(False)
		textview.set_border_width(2)
		self.textbuffer = textview.get_buffer()
		sw.add(textview)
		sw.show()
		textview.show()
		vbox.pack_end(sw, False, False, 0)


		# Muestra la ventana
		self.show()


	# Apartado de sockets
	def startService(self, widget, socket_direction="localhost", socket_port=9999):
		""""""
		self.s = socket.socket()
		self.s.bind((socket_direction, socket_port))
		self.s.listen(1)
		self.sc, self.addr = self.s.accept()
		
		while True:
			recibido = self.sc.recv(1024)
			print "Recibido:", recibido
			final = self.textbuffer.get_end_iter()
			entry_text = recibido + "\n"
			
			#Insertamos texto en el textbox de informacion (como prueba)
			self.textbuffer.insert(final, entry_text)
			self.sc.send(recibido)
			
		return False	

	# Cierre de aplicacion
	def quit(self, dialog=None, response=None):
		""""""
		try:
			self.sc.close()
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
