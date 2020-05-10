import hangman
import reversegam
import tictactoeModificado     #Modifique los main() de los juegos para que retornen el tiempo de juego y si logro ganar.
import json
import os
import PySimpleGUI as sg

#Utilizo un diccionario como estructura de datos donde cada clave es un nombre para que sea facil
#encontrar la información de un jugador especifico.Los elementos de este diccionario son listas ,donde cada elemento
#de la lista es un diccionario con la información de el juego que jugo,el tiempo de juego y si logro ganar.

#Elegí usar un formato json porque me permite almacenar el diccionario de una forma que sea facil de leer.


def si_existe_archivo():
	#Se pregunta si el archivo existe
	if os.path.isfile('archivoJugadores.json'):
		#Si existe se abre como lectura y se cargan los datos que ya tenia el archivo
		archivo_jugadores=open('archivoJugadores.json',"r")
		datos=json.load(archivo_jugadores)
		archivo_jugadores.close()
	else:
		datos={}
	return datos

def agregar_a_lista(datos,nombre_jugador):
	aux=[]
	#Se agrega a una lista los juegos que jugo
	for i in datos[nombre_jugador]:
		aux.append(i["Juego"])
	return aux
	
def cambiar_marca_tiempo(datos,nombre_jugador,juego,tiempo_juego,gano):
	indice=0
	ok=True
	#Si gano ,se guardara el nuevo tiempo solo si mejoro su mejor marca de tiempo hasta ahora o si todavía no habia ganado.
	if(gano):
		while ok and indice<len(datos[nombre_jugador]) :
			#Se busca el juego en la lista ,se pregunta si ya habia ganado y si mejoro su tiempo se actualiza el tiempo.
			if datos[nombre_jugador][indice]["Juego"]==juego and datos[nombre_jugador][indice]["Gano"]==True and float(datos[nombre_jugador][indice]["Tiempo Juego"][0:3])>tiempo_juego:
				datos[nombre_jugador][indice]["Tiempo Juego"]=str(round(tiempo_juego,1))+" seg"
				ok=False
			#Si no habia ganado todavía se actualiza Gano en True y se asigna el tiempo.
			elif datos[nombre_jugador][indice]["Juego"]==juego and datos[nombre_jugador][indice]["Gano"]==False:
				datos[nombre_jugador][indice]["Tiempo Juego"]=str(round(tiempo_juego,1))+" seg"
				datos[nombre_jugador][indice]["Gano"]=True
				ok=False
			indice=indice+1
	
	
def pasar_a_archivo(nombre_jugador,juego,tiempo_juego,gano):
	#Función que retorna los datos del archivo si este existe.
	datos=si_existe_archivo()
	#Si el nombre del jugador ya existe
	if nombre_jugador in datos:
		#Funcion que retorna una lista con los juegos que jugo
		aux=agregar_a_lista(datos,nombre_jugador)
		#Si el jugador no jugo anteriormente a ese juego,se agrega ese juego y se ordena por nombre del juego.
		if not juego in aux:
			datos[nombre_jugador].append({"Juego":juego,"Tiempo Juego":str(round(tiempo_juego,1))+" seg","Gano":gano})
			datos[nombre_jugador]=sorted(datos[nombre_jugador],key=lambda juego:juego["Juego"])
		else:
			#Sino
			#Función para actualizar el tiempo.
			cambiar_marca_tiempo(datos,nombre_jugador,juego,tiempo_juego,gano)
	else:
		#Sino,se agrega ese jugador
		datos[nombre_jugador]=[{"Juego":juego,"Tiempo Juego":str(round(tiempo_juego,1))+" seg","Gano":gano}]
	archivo_jugadores=open("archivoJugadores.json","w")#Se abre el archivo en modo escritura para escribir los datos en el archivo.
	#Se escribe el archivo con los datos actualizados y ordenados por nombre.
	json.dump(datos,archivo_jugadores,indent=4,sort_keys=True)
	archivo_jugadores.close()

def main(args):
	#Se declara el layout
	layout=[
	[sg.Text("Ingrese nombre"),sg.InputText(key="Nombre")],
	[sg.Text('Seleccione Un Juego',size=(50,1))],
	[sg.Button("Ahorcado",size=(50,1))],
	[sg.Button("Ta-Te-Ti",size=(50,1))],
	[sg.Button("Otello",size=(50,1))],
	[sg.Button("Salir")],
	]
	ok=True
	window=sg.Window('JUEGOS',layout)
	while ok:
		#Se leen los eventos
		evento,valores=window.read()
		#Si el evento es salir o X  se cierra la ventana
		if evento==None or evento=="Salir":
			ok=False
		#Sino ,si hay un nombre ingresado se empieza a jugar el juego que escogio.
		elif valores["Nombre"]!="":
			#Se minimiza la ventana asi solo aparece la consola con el juego.
			window.Minimize()
			valores["Nombre"]=valores["Nombre"].capitalize()
			#Se juega el juego que escogio el jugador ,y se pasa a la funcion pasar_a_archivo su información
			if evento=="Ahorcado":
				tiempo_juego,gano=hangman.main()
				pasar_a_archivo(valores["Nombre"],"Ahorcado",tiempo_juego,gano)
			elif evento=="Ta-Te-Ti":
				tiempo_juego,gano=tictactoeModificado.main()
				pasar_a_archivo(valores["Nombre"],"Ta-Te-Ti",tiempo_juego,gano)
			elif evento=="Otello":
				tiempo_juego,gano=reversegam.main()
				pasar_a_archivo(valores["Nombre"],"Otello",tiempo_juego,gano)
			#Vuelve a aparecer la ventana
			window.Normal()
		
	

		
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
