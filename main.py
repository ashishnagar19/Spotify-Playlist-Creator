import export as export
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
client_id_env = os.environ.get('CLIENT-ID')
client_secret_env = os.environ.get('CLIENT_SECRET')

#scrapping
date = input("Enter the date for which you want to heard the songs:")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
data = response.text
soup = BeautifulSoup(data, "html.parser")
songs = soup.find_all(name="h3", class_="a-no-trucate")
songs_name = [song.getText().strip("\n\t") for song in songs]

#authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private", redirect_uri='http://example.com', client_id=client_id_env,
                                                    client_secret=client_secret_env, show_dialog=True, cache_path="token.txt"))
user_id = sp.current_user()["id"]
print(user_id)

#searching songs
song_uris = []
year = date.split("-")[0]
for song in songs_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)






