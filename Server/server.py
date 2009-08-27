import socket
import select 
import time
import os
import sys

#Clase servidor, crea un nuevo servidor.
class Servidor:
	#Inicializacion de variables, se ejecuta cuando se invoca una instancia de la clase servidor
	def __init__(self, p):
		print "Servidor en escucha..."
		self.puerto=p
	
	#Intenta recibir y componer el avatar del usuario
	def avatar(self, sock):
		file = open("avatar.jpg", "wb")
		parte=sock.recv(128)
	
	#Devuelve el nick de la gente conectada
	def conectados(self, nicks,sock):
		for nick in nicks:		
			sock.send(nicks[nick]+"\n")
	
	#Comprueba si se recibe un mensaje del sock, si no responde se entiende que se ha desconectado y se elimina
	def recibir(self, listaSockets, sock, nicks):
		try:
			mensaje = sock.recv(1024)
			sock.settimeout(.1)
			return mensaje
		except:
			listaSockets.remove(sock)
			del nicks[sock] #No funciona bien, solucionar
			sock.close()
			return None
	
	#Comprueba nuevas conexiones de clientes y agrega su sock a la lista.
	def conectar(self, servidor, listaSockets, nicks):
		try:
			scliente, addr = servidor.accept()
			servidor.settimeout(.1)
			dir=addr[0]	
			scliente.send("#######################################\n")
			scliente.send("Bienvenido a la v.1.0 de Pyim\n")
			scliente.send("#######################################\n\n")
			
			#La cadena de conexion debe tener la siguiente forma:
			#nick-avatar siendo [avatar] 'y' o 'n' segun tenga o no avatar
			#conexion_string=scliente.recv(1024)
			
			#i=0
			#while conexion_string[i] != '-':
			#	cnick=cnick+conexion_string[i]
			#	i++
			
			#avatar=conexion_string[i+1]
			
			#if avatar == 'y':
			#	self.avatar(scliente)
				
			cnick=scliente.recv(1024)
			nicks[scliente]=cnick
			listaSockets.append(scliente)
			
			for destino in listaSockets:
				if destino != servidor and destino != scliente:
					destino.send(cnick)
					destino.send(" se ha conectado.\n") #Arreglar salto de linea 
		except:
			pass

	#Envia el mensaje del sock al resto de clientes
	def enviar(self, listaSockets, servidor, sock, mensaje, nicks):
		hora=time.localtime(time.time())
		for destino in listaSockets:
			if destino != servidor and destino != sock:
				destino.send("["+str(hora[3])+":"+str(hora[4])+":"+str(hora[5])+"] ")	
				destino.send(nicks[sock])
				destino.send(" dice: "+mensaje+"\n")
				
	#Comprueba si el mensaje es un comando valido			
	def Comp_Comando(self, mensaje, nicks, sock, listaSockets, servidor):
		salida=False
		if '@conectados' in mensaje:
			salida=True
			self.conectados(nicks, sock)
		elif '@salir' in mensaje:
			salida=True
			for destino in listaSockets:
				if destino != servidor and destino != sock:
					destino.send(nicks[sock])
					destino.send(" se ha desconectado.\n") #Arreglar salto de linea 
			
			listaSockets.remove(sock)
			del nicks[sock]
			sock.close()
			
		elif '@comandos' in mensaje:
			salida=True
			sock.send("@conectados\n@salir\n@afk\n")
		elif '@afk' in mensaje:
			salida=True
			for destino in listaSockets:
				if destino != servidor and destino != sock:
					destino.send(nicks[sock])
					destino.send(" esta AFK.\n")
		return salida
	
	#Redirecciona la salida de error a un archivo de texto (TODO)
	def log(self):
		print "Hola"
				
	#Inicializa el servidor y realiza toda la rutina			
	def ejecutar(self):
		servidor=socket.socket()
		listaSockets=[servidor]
		nicks={}

		servidor.bind(("", self.puerto))
		
		servidor.listen(50)
		salir=False
		while salir==False:
				self.conectar(servidor, listaSockets, nicks)
				(sread, swrite, sexc)=select.select(listaSockets, [], [])
				for sock in sread:
					if sock != servidor:
						mensaje=self.recibir(listaSockets, sock, nicks)
						if mensaje!=None:
							comando=self.Comp_Comando(mensaje, nicks, sock, listaSockets, servidor)
							if comando==False:
								if '@chipiritiflautico' in mensaje:
									salir=True
								else:
									self.enviar(listaSockets, servidor, sock, mensaje, nicks)
		servidor.close()
		
		
def main():
	
	servername=Servidor(int(sys.argv[1]))
	servername.ejecutar()	
	
	return 0

if __name__ == '__main__':
	main()
