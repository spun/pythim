#! /usr/bin/env python

import socket

class newSocket:
	""""""
	def __init__(self, dialogo, gobjectGUI, host="localhost", port=9999, user="Anonimo"):

		# self.dialogo es la ventana de conversacion
		self.conversacion = dialogo
		
		info_conex= "Se intentara conectar a " + host+":" + str(port) + " como " + user
		self.conversacion.set_text(info_conex)
		
		try:
			self.s = socket.socket()
			self.s.connect((host, port))
			self.s.send(user)
			gobjectGUI.idle_add(self.recv_text)
			start_text="\nConectado\n\n"
			color = "green"

		except:
			start_text="\nNo se pudo conectar\n\n"
			color = "red"
                        
		final = self.conversacion.get_end_iter()
		startiter =  self.conversacion.get_end_iter().get_offset()

		self.conversacion.insert(self.conversacion.get_iter_at_offset(startiter), start_text)
		startiter = self.conversacion.get_iter_at_offset(startiter)
		enditer = self.conversacion.get_end_iter()
                
		tag = self.conversacion.create_tag(None, foreground = color)
		self.conversacion.apply_tag(tag, startiter, enditer)


	def send_mens(self, text):
		print text
		try:
			self.s.send(text)

		except:
			final = self.conversacion.get_end_iter()
			self.conversacion.insert(final,"\n Ocurrio un error al enviar el mensaje")
			self.conversacion.insert(final,text)



  	def recv_text(self):
		#print "rec"
		try:
			mensaje=self.s.recv(1024)
			self.s.settimeout(.1)
			final = self.conversacion.get_end_iter()
			self.conversacion.insert(final,mensaje)
			return True
		except:
			return True


	def desconectar(self):
		print "Fin SOCKET"
  		self.s.send("@salir")
		self.s.close()
