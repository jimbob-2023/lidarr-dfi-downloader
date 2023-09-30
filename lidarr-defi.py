import requests
import subprocess
import json
import base64
import requests
from urllib.parse import quote
SPOTIFY_CLIENT_ID = 'REPLACEME'
SPOTIFY_CLIENT_SECRET = 'REPLACEME'
LIDARR_API_URL = "http://localhost:8686/api/v1"
LIDARR_API_KEY = 'REPLACEME'
SPOTIFY_ALBUMS_FILE = 'spotify_albums.txt'
SPOTIFY_TRACKS_FILE = 'spotify_tracks.txt'
def fetch_missing_tracks_from_lidarr():
    all_missing_tracks = []

    try:
        BASE_URL = 'http://localhost:8686/api/v1/wanted/missing?includeArtist=true'
        results_per_page = 10  # Adjust this as needed based on the API's behavior.
        
        page = 1
        while True:
            response = requests.get(f"{BASE_URL}&pageSize={results_per_page}&page={page}", headers={'X-Api-Key': LIDARR_API_KEY})
            response.raise_for_status()

            missing_items_page = response.json()
            records = missing_items_page.get('records', [])

            # Filter out only singles
            singles = [record for record in records if record.get("albumType") == "Single"]
            all_missing_tracks.extend(singles)

            # If there are no records or fewer records than expected, we've reached the end.
            if not records or len(records) < results_per_page:
                break

            page += 1

    except requests.RequestException as e:
        print(f"Error fetching missing tracks from Lidarr: {e}")

    return all_missing_tracks

def fetch_missing_albums_from_lidarr():
    all_missing_albums = []

    try:
        BASE_URL = 'http://localhost:8686/api/v1/wanted/missing?includeArtist=true'
        results_per_page = 10  # Adjust this as needed based on the API's behavior.
        
        page = 1
        while True:
            response = requests.get(f"{BASE_URL}&pageSize={results_per_page}&page={page}", headers={'X-Api-Key': LIDARR_API_KEY})
            response.raise_for_status()

            missing_items_page = response.json()
            records = missing_items_page.get('records', [])

            # Filter out only albums and EPs
            albums_and_eps = [record for record in records if record.get("albumType") in ["Album", "EP"]]
            all_missing_albums.extend(albums_and_eps)

            # If there are no records or fewer records than expected, we've reached the end.
            if not records or len(records) < results_per_page:
                break

            page += 1

    except requests.RequestException as e:
        print(f"Error fetching missing albums from Lidarr: {e}")

    return all_missing_albums

def save_spotify_urls_to_file(urls, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(f"{url}\n")

def search_spotify_for_album_tracks(album_data):
    token = get_spotify_access_token()
    album_urls = []  # Renaming this to album_urls for clarity

    for album in album_data:
            album_name = album.get("title")
            if not album_name:
                continue

            # Search for the album on Spotify
            response = requests.get(
                f"https://api.spotify.com/v1/search?q={quote(album_name)}&type=album&limit=1",
                headers={"Authorization": "Bearer " + token}
            )
            response.raise_for_status()

            search_results = response.json()

            # Extract the search results
            items = search_results.get('albums', {}).get('items', [])

            if items:
                album = items[0]
                album_name = album.get('name')
                artist_name = album['artists'][0].get('name')
                spotify_uri = album.get('uri')

                if spotify_uri:
                    spotify_url = uri_to_url(spotify_uri)
                    album_urls.append(spotify_url)

                print(f"Found album: {album_name} by {artist_name}")

    save_spotify_urls_to_file(album_urls, SPOTIFY_ALBUMS_FILE)

def get_spotify_access_token():
    auth_string = (SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET).encode('utf-8')
    base64_encoded = base64.b64encode(auth_string).decode('utf-8')
    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": "Basic " + base64_encoded},
        data={"grant_type": "client_credentials"}
    )

    auth_response.raise_for_status()
    return auth_response.json().get('access_token')

def uri_to_url(uri):
    parts = uri.split(":")
    return f"https://open.spotify.com/{parts[1]}/{parts[2]}"

def save_spotify_track_urls_to_file(track_urls):
    with open('spotify_tracks.txt', 'w', encoding='utf-8') as tracks_file:
        for track_url in track_urls:
            tracks_file.write(f"{track_url}\n")

def search_spotify_for_tracks(track_data):
    """
    Search Spotify for a list of track names.
    For each track name found, it prints the track and artist name.
    Then, it saves the Spotify URL to a file.
    """

    # Get Spotify Access Token
    token = get_spotify_access_token()
    track_urls = []

    for track in track_data:
        track_name = track.get("title")  # Adjust this key as needed based on the structure of your data
        if not track_name:
            continue

        # Search for the track on Spotify
        response = requests.get(
            f"https://api.spotify.com/v1/search?q={quote(track_name)}&type=track&limit=1",
            headers={"Authorization": "Bearer " + token}
        )
        response.raise_for_status()

        search_results = response.json()

        # Extract the search results
        items = search_results.get('tracks', {}).get('items', [])

        if items:
            track = items[0]
            track_name = track.get('name')
            artist_name = track['artists'][0].get('name')
            spotify_uri = track.get('uri')

            if spotify_uri:
                spotify_url = uri_to_url(spotify_uri)
                track_urls.append(spotify_url)

            print(f"Found track: {track_name} by {artist_name}")

    # Save the Spotify URLs to a file
    save_spotify_urls_to_file(track_urls, SPOTIFY_TRACKS_FILE)

def download_tracks_from_file():
    with open('spotify_tracks.txt', 'r', encoding='utf-8') as tracks_file:
        for line in tracks_file:
            track_url = line.strip()
            if track_url:
                d_fi_download(track_url)

def download_albums_from_file():
    with open(SPOTIFY_ALBUMS_FILE, 'r', encoding='utf-8') as albums_file:
        for line in albums_file:
            album_url = line.strip()
            if album_url:
                d_fi_download(album_url)

def d_fi_download(track_url):
    command = [".\\d-fi.exe", "-q", "320", "-u", track_url, "-d", "-conf", "config.json"]
    try:
        result = subprocess.run(command, capture_output=True, encoding='utf-8', check=True)
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error during d-fi execution: {e}")
        print(e.stderr)  # print the stderr instead of e.output

    except UnicodeDecodeError:
        # If there's an encoding issue, this will capture it
        print("There was an error decoding the output from d-fi.")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Handle missing tracks
    missing_tracks = fetch_missing_tracks_from_lidarr()
    search_spotify_for_tracks(missing_tracks)

    # Handle missing albums
    missing_albums = fetch_missing_albums_from_lidarr()
    search_spotify_for_album_tracks(missing_albums)

    download_tracks_from_file()
    download_albums_from_file()  # Download albums as well

