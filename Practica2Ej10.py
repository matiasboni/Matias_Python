imagenes=['im1','im2','im3'] 
nueva_lista=[]
#Se realiza un for de la cantidad de imagenes
for i in range(len(imagenes)):
	sigue=True
	#Mientras se tengan que ingresar coordenadas porque no son validas 
	while(sigue):
		x=input("Escriba una coordenada x: ")
		y=input("Escriba una coordenada y: ")
		valida=True
		#Se busca las coordenadas en la nueva lista
		for indice in range(len(nueva_lista)):
			if(nueva_lista[indice][1][0]==x)and(nueva_lista[indice][1][2]==y):
				valida=False
		#Si la coordenada es valida o no hay elementos en la lista ,se agrega la coordena
		if(valida)or(not nueva_lista):
			nueva_lista.append([imagenes[i],x+","+y])
			#Se le asigna el valor de falso para no continuar leyendo coordenadas para esa imagen
			sigue=False
		#Sino se avisa que la coordenada no es valida 
		else:
			print("Coordenada no valida")
#Se imprime la nueva lista con las coordenadas
print(nueva_lista)
						
				
