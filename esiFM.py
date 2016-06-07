#!/usr/bin/python
#-*- encoding: utf-8 -*-
import conexionTwitter
import conexionYoutube
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from bs4 import BeautifulSoup
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import urllib, unicodedata
from flask import Flask, render_template

twitter_api =  conexionTwitter.oauth_login()

#Nota: Los metodos que obtienen las canciones funcionan de la misma manera, por tanto se comentará solamente el de 
#la lista radiole.

# Método que nos devuelve un array con las canciones actuales en la lista de radiole
def ListaRadiole():
	# Asignamos la url de dicha lista a una variable
	direcc = "http://www.radiole.com/lista-radiole" 
	# Leemos el código html gracias al modulo urllib
	page = urllib.urlopen(direcc).read() 
	# Utilizaremos beautifulsoup para la extracción de datos
	sopa = BeautifulSoup(page,'lxml')  
	# Luego utilizamos el método findAll de BeautifulSoup para que nos encuentre todos las etiquetas div que tengan una
	# class itm-body ya que en esta página las canciones de la lista se encuentran dentro de esta etiqueta
	canciones_lista = sopa.findAll('div',class_="itm-body")
	# Creamos un array para añadir las canciones
	array_canciones = []
	# Ahora recorreremos el array que hemos obtenido con el metodo findAll de BeautifulSoup ya que puede haber alguna 
	# etiqueta div con la misma clase pero no tener dentro ninguna cancion
	for cancion in canciones_lista:
		# Estudiando el código nos damos cuenta que la etiqueta div contiene canciones si dentro tiene una etiqueta p, por lo 
		# tanto, hacemos la siguiente comprobación
		if(cancion.find('p')):
			b = cancion.find('p').text.capitalize() # Ponemos en mayúscula sólo la primera letra del título de la canción para que no haya conflicto al comparar
			array_canciones.append(b) # Añadimos la canción al array
	return array_canciones

# Método que devuelve un array con las canciones actuales en la lista de los 40 principales
def ListaLos40():
	direcc4 = "http://los40.com/lista40/"
	page4 = urllib.urlopen(direcc4).read()
	sopa4 = BeautifulSoup(page4,'lxml')
	canciones_lista4 = sopa4.findAll('div',class_="info_grupo")

	array_canciones4 = []

	for cancion in canciones_lista4:
		if(cancion.find('p')):
			b = cancion.find('p').text.capitalize() # Ponemos en mayúscula sólo la primera letra del título de la canción para que no haya conflictos al comparar
			array_canciones4.append(b) # Añadimos la cancion al array
	return array_canciones4

# Método que devuelve un array con las canciones actuales en la lista de Hitfm
def ListaHitfm():
	direccHit = "http://www.musiclist.es/hit-fm"
	pageHit = urllib.urlopen(direccHit).read()
	sopaHit = BeautifulSoup(pageHit,'lxml')
	canciones_listaHit = sopaHit.findAll('div',class_="col-xs-8 item-chart-ol")
	array_canciones_hit = []

	for cancion in canciones_listaHit:
		if(cancion.find('h4')):
			b = cancion.find('h4').text.capitalize() # Ponemos en mayúscula sólo la primera letra del título de la canción para que no haya conflictos al comparar
			array_canciones_hit.append(b) # Añadimos la cancion al array
	return array_canciones_hit

# Método que devuelve un array con las canciones actuales en la lista de EuropaFm
def ListaEuropafm():
	direccEu = "http://www.musiclist.es/hit-fm"
	pageEu = urllib.urlopen(direccEu).read()
	sopaEu = BeautifulSoup(pageEu,'lxml')
	canciones_listaEu = sopaEu.findAll('div',class_="col-xs-8 item-chart-ol")
	array_canciones_eu = []

	for cancion in canciones_listaEu:
		if(cancion.find('h4')):
			b = cancion.find('h4').text.capitalize() # Ponemos en mayúscula sólo la primera letra del título de la canción para que no haya conflictos al comparar
			array_canciones_eu.append(b) # Añadimos la cancion al array
	return array_canciones_eu

# Método que devuelve las canciones en común que suenan en las diferentes emisoras
def ListaComunes():
	# Creamos un array para añadir las canciones comunes que vaya encontrando
	array_canciones_comunes = []
	# Creamos los arrays con las llamadas a los diferentes métodos que hemos creado anteriormente
	array_radiole = ListaRadiole()
	array_los40 = ListaLos40()
	array_hitfm = ListaHitfm()
	array_europafm = ListaEuropafm()

	# Buscamos las canciones comunes que suenan en las distintas emisoras, si las encuentra las añadimos al array de canciones comunes
	for cancion in array_europafm:
		if (cancion in array_los40 and cancion in array_hitfm):
			array_canciones_comunes.append(cancion)

	return array_canciones_comunes

print("---------------Lista canciones comunes---------------------------------------------------------")
array_comunes = ListaComunes()
print(array_comunes)

primera = array_comunes[0] + "\n"
segunda = array_comunes[1] + "\n"
tercera = array_comunes[2] + "\n"

twitter_api.statuses.update(status= "Estas son las 3 canciones que lo petan en tus emisoras de radio:\n"+primera+segunda+tercera)

# Obtenemos el id de los videos para poder pasarlos a la pagina web y visualizarlos en ella
codVideos = []
for i in array_comunes:
	try:
		codVideos.append(conexionYoutube.youtube_search(i, 1)) 
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


# Obtenemos el total de reproducciones de cada canción

totalReproducciones = []
for item in codVideos:
	totalReproducciones.append(int(item[0][2])/1000000)

# PASANDO PARAMETROS A LA PAGINA

app = Flask(__name__)

@app.route("/")
def cargaWeb():
	return render_template('index.html', datos = codVideos)
	
if __name__ == "__main__":
    app.run(debug=False)
