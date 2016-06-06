#!/usr/bin/python
#-*- encoding: utf-8 -*-
from apiclient.discovery import build
import json
import requests
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

#Nos registramos en youtube y obtenemos los credenciales necesarios para usar la API

DEVELOPER_KEY = "AIzaSyBysg7aCtvYb11WtqR9AVGTQy1p5B8waHA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Utilizamos el siguiente metodo de la api para buscar las canciones comunes que hemos obtenido a través de BeautifulSoup
# también obteniendo los ids de las canciones para luego poder mostrarlas en la pagina web.
def youtube_search(query, max_results):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	developerKey=DEVELOPER_KEY)

	# Llama al método search.list para ver lo resultados que coinciden con el término de consulta especificada
	search_response = youtube.search().list(
	q=query,
	part="id,snippet",
	maxResults=max_results
	).execute()

	datos = []
	datos.append([0]*3)

	# Añadir cada resultado a la lista apropiada
	# Búsqueda de vídeos, canales, y lista de reproducción.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			datos[0][0] = search_result["snippet"]["title"]
			datos[0][1] = search_result["id"]["videoId"]
			# Hacemos un request para recuperar el total de reproducciones
			r = requests.get('https://www.googleapis.com/youtube/v3/videos?id='+datos[0][1]+'&key=AIzaSyBysg7aCtvYb11WtqR9AVGTQy1p5B8waHA&part=statistics')
			a = json.loads(r.text)
			datos[0][2] = a['items'][0]['statistics']['viewCount']
		  	return datos
		elif search_result["id"]["kind"] == "youtube#channel":
		  return("%s (%s)" % (search_result["snippet"]["title"],
				                       search_result["id"]["channelId"]))
		elif search_result["id"]["kind"] == "youtube#playlist":
		  return("%s (%s)" % (search_result["snippet"]["title"],
				                        search_result["id"]["playlistId"]))

