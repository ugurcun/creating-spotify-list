from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


URL = "https://www.billboard.com/charts/hot-100/1996-08-14/"

CLIENT_ID = ""
CLIENT_SECRET = ""

DATE = input("which year do you want to travel? (type YYYY-MM-DD format.): ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + DATE)

soup = BeautifulSoup(response.text, "html.parser")
song_names_span = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
song_names = [song.getText().strip("\n\t") for song in song_names_span]
# print(song_names)



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        cache_path="token.txt",
        show_dialog=True
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = DATE.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} does not exist in spotify. Skipped.")

# print(user_id)
name_of_playlist = "yarrakbatu"
playlist = sp.user_playlist_create(user=user_id, name=name_of_playlist, public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


