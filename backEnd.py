import billboard
import requests
from random import randint
from pprint import pprint

previously_used = []

#Gets a random Number.
#If already in the list, get another.
#If not, add it to the list and return it.
#This guarantees the same songs are not reused.
def random_index():
	x = randint(1,100)
	while x in previously_used:
		x = randint(1,100)
	
	previously_used.append(x)
	return x


#Given a number,
	#Finds the spotify track data for it in json format 
	#using the billboard and Spotify API.
#Only takes numbers 1-100.
def get_track_data(i):
	cd = billboard.ChartData("hot-100")
	song = cd[i-1]
	uri = song.spotifyLink
	track_id = uri[uri.index("k:")+2:]
	
	track = requests.get("https://api.spotify.com/v1/tracks/"+track_id, timeout=5)
	jsonData = track.json()
	return jsonData

#Given the json dump for some song,
	#finds the song on spotify, 
	#and downloads the mp3 sample for it.
#If the chosen song data lacks an mp3 url, an Error will be raised. 
	#Just run it again if this happens.
def download_mp3(jsonData):
	mp3_url = jsonData["preview_url"]
	if mp3_url == None:
		raise TypeError
	track_name = jsonData["name"]
	import urllib.request
	urllib.request.urlretrieve(mp3_url, "Songs/"+track_name+".mp3")

#Download an artist's image
def download_pic(artist_ID):
	jsonData = requests.get("https://api.spotify.com/v1/artists/"+artist_ID).json()
	picture_url = jsonData["images"][0]["url"]
	artist = jsonData["name"]
	import urllib.request
	urllib.request.urlretrieve(picture_url, "Pics/"+artist+"Pic.png")

#For an artist, get some songs.
#can throw a ValueError
def getOtherSongs(artist_ID, real_song_name):
	response = requests.get("https://api.spotify.com/v1/artists/"+artist_ID+"/top-tracks"+"?country=ES")
	jsonData = response.json()
	track_list = jsonData["tracks"]
	return [each_song["name"] for each_song in track_list if each_song["name"].lower() != real_song_name.lower()]

#Just for testing.
if __name__ == "__main__":
	songJSON = get_track_data(random_index())
	pprint(songJSON)