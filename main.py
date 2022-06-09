import os
from bs4 import BeautifulSoup
import requests
import os
import spotipy 
from spotipy.oauth2 import SpotifyOAuth

#Keys for spotifyOAuth
clientKey = os.environ.get("CLIENTID")
secretKey = os.environ.get("CLIENTSECRT")

#Input for date of songs to get
date = input("Input the year month and day in the format of YYYY-MM-DD to search for a specific date of songs: ")

#get request to get the text
list = requests.get("https://www.billboard.com/charts/japan-hot-100/" + date).text

#get contents with beautifulsoup then select only songs
soup = BeautifulSoup(list, "html.parser")
contents = soup.select("li #title-of-a-story")
scope = "playlist-modify-private"

#spotify Authetication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id = clientKey,
        client_secret=secretKey,
        redirect_uri="",
        show_dialog=True,
        cache_path="",
        scope=scope))

#Getting the date of year
date = list.split("-")[0]

#song uri final
songURIs = []

#search if song exist
for song in contents:
    search = sp.search(q=f"track:{song.getText().split()} year:{date}", type="track")
    try:
        uri = search["tracks"]["items"][0]["uri"]
        songURIs.append(uri)
    except IndexError:
        pass

#for first intance
#sp.playlist_add_items(playlist_id="https://open.spotify.com/playlist/4CWzu14u70eXGt9xKDrfTZ?si=9542e3ce50db43a1", items=songURIs)
    
#after to get a new playlist each day or for whatever
sp.playlist_replace_items(playlist_id="https://open.spotify.com/playlist/4CWzu14u70eXGt9xKDrfTZ?si=9542e3ce50db43a1", items=songURIs)