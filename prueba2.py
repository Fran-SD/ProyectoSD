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

#funcion para eliminar tildes y caracteres raros
"""def elimina_tildes(s): 
	return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))"""

twitter_api =  conexionTwitter.oauth_login()

#canciones lista radiole

def ListaRadiole():
	direcc = "http://www.radiole.com/lista-radiole"
	page = urllib.urlopen(direcc).read()
	sopa = BeautifulSoup(page,'lxml')
	canciones_lista = sopa.findAll('div',class_="itm-body")

	array_canciones = []

	for cancion in canciones_lista:
		if(cancion.find('p')):
			#a = elimina_tildes(cancion.find('p').text) #eliminamos tildes en caso de que existan en el nombre de la cancion
			b = cancion.find('p').text.capitalize() #Ponemos en mayuscula solo la primera letra del titulo de la cancion para que no haya conflicto al comparar
			array_canciones.append(b) #añadimos la cancion al array
	print("----------------Lista Radiole---------------------------------------------------------------")
	print array_canciones
	return array_canciones
		
"""for item in array_canciones:
	print item,"\n"""

print("----------------Lista Radiole---------------------------------------------------------------")
#print(array_canciones)
#canciones lista 40 principales
def ListaLos40():
	direcc4 = "http://los40.com/lista40/"
	page4 = urllib.urlopen(direcc4).read()
	sopa4 = BeautifulSoup(page4,'lxml')
	canciones_lista4 = sopa4.findAll('div',class_="info_grupo")

	array_canciones4 = []

	for cancion in canciones_lista4:
		if(cancion.find('p')):
			#a = elimina_tildes(cancion.find('p').text) #eliminamos tildes en caso de que existan en el nombre de la cancion
			b = cancion.find('p').text.capitalize()#Ponemos en mayuscula solo la primera letra del titulo de la cancion para que no haya conflicto al comparar
			array_canciones4.append(b)

	return array_canciones4

print("---------------Lista 40 principales---------------------------------------------------------")
#print(array_canciones4)

def ListaHitfm():
	direccHit = "http://www.musiclist.es/hit-fm"
	pageHit = urllib.urlopen(direccHit).read()
	sopaHit = BeautifulSoup(pageHit,'lxml')
	canciones_listaHit = sopaHit.findAll('div',class_="col-xs-8 item-chart-ol")
	array_canciones_hit = []

	for cancion in canciones_listaHit:
		if(cancion.find('h4')):
			#a = elimina_tildes(cancion.find('h4').text) #eliminamos tildes en caso de que existan en el nombre de la cancion
			b = cancion.find('h4').text.capitalize()#Ponemos en mayuscula solo la primera letra del titulo de la cancion para que no haya conflicto al comparar
			array_canciones_hit.append(b) #añadimos la cancion al array
	#print("---------------Lista HIT FM---------------------------------------------------------")
	#print (array_canciones_hit)
	return array_canciones_hit

print("---------------Lista HIT FM---------------------------------------------------------")
#print(array_canciones_hit)

def ListaEuropafm():
	direccEu = "http://www.musiclist.es/hit-fm"
	pageEu = urllib.urlopen(direccEu).read()
	sopaEu = BeautifulSoup(pageEu,'lxml')
	canciones_listaEu = sopaEu.findAll('div',class_="col-xs-8 item-chart-ol")
	array_canciones_eu = []

	for cancion in canciones_listaEu:
		if(cancion.find('h4')):
			#a = elimina_tildes(cancion.find('h4').text) #eliminamos tildes en caso de que existan en el nombre de la cancion
			b = cancion.find('h4').text.capitalize()#Ponemos en mayuscula solo la primera letra del titulo de la cancion para que no haya conflicto al comparar
			array_canciones_eu.append(b) #añadimos la cancion al array
	return array_canciones_eu

print("---------------Lista EUROPA FM---------------------------------------------------------")

def ListaMaximafm():
	direccMax = "http://www.musiclist.es/maxima-fm"
	pageMax = urllib.urlopen(direccMax).read()
	sopaMax = BeautifulSoup(pageMax,'lxml')
	canciones_listaMax = sopaMax.findAll('div',class_="col-xs-8 item-chart-ol")
	array_canciones_max = []

	for cancion in canciones_listaMax:
		if(cancion.find('h4')):
			#a = elimina_tildes(cancion.find('h4').text) #eliminamos tildes en caso de que existan en el nombre de la cancion
			b = cancion.find('h4').text.capitalize()#Ponemos en mayuscula solo la primera letra del titulo de la cancion para que no haya conflicto al comparar
			array_canciones_max.append(b) #añadimos la cancion al array
	print("---------------Lista Maxima FM---------------------------------------------------------")
	print(array_canciones_max)
	return array_canciones_max


#print(array_canciones_eu)

def ListaComunes():
	array_canciones_comunes = []

	array_radiole = ListaRadiole()
	array_los40 = ListaLos40()
	array_hitfm = ListaHitfm()
	array_europafm = ListaEuropafm()
	array_maximafm = ListaMaximafm()

	for cancion in array_europafm:
		if (cancion in array_los40 and cancion in array_hitfm and cancion in array_maximafm):
			array_canciones_comunes.append(cancion)
	print("---------------Lista canciones comunes---------------------------------------------------------")
	print(array_canciones_comunes)
	return array_canciones_comunes


array_comunes = ListaComunes()
print(array_comunes)
"""for i in range(0,3):
	print  array_comunes[i],"\n"""


"""primera = array_comunes[0] + "\n"
segunda = array_comunes[1] + "\n"
tercera = array_comunes[2] + "\n"

twitter_api.statuses.update(status= "Disfruta de las canciones mas sonadas en tus emisoras de radio:\n"+primera+segunda+tercera)"""

print "Videos:\n"
codVideos = []
for i in array_comunes:
	try:
		codVideos.append(conexionYoutube.youtube_search(i, 1))
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


# Diagrama de barras

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

totalReproducciones = []
for item in codVideos:
	totalReproducciones.append(int(item[0][2])/1000000)
	#print totalReproducciones
			
#print len(array_canciones_comunes)
#print len(totalReproducciones)

posicion_y = np.arange(len(array_comunes))
plt.figure(figsize=(20,10))
plt.barh(posicion_y, totalReproducciones, align = "center")
plt.yticks(posicion_y, array_comunes)
plt.xlabel("Total reproducciones (millones)")
plt.title("Reproducciones en Youtube")
plt.xlim(1, 500, 100)
plt.savefig("grafica.png")

#PASANDO PARAMETROS A LA PAGINA
		
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def cargaWeb():
	return render_template('index.html', datos = codVideos)
	
if __name__ == "__main__":
    app.run(debug=False)
    

