# Lidarr D-FI Downloader

This script automatically fetches missing tracks and albums from your Lidarr setup and searches them on Spotify. If found, it prepares a list of URLs to be downloaded using [d-fi](https://github.com/spotDL/d-fi), a Spotify downloader tool.

## Prerequisites

- A working installation of [Lidarr](https://lidarr.audio/).
- A Spotify developer account to create API access.
- [d-fi](https://notabug.org/sayem314/d-fi) set up and ready for downloading tracks from Spotify.

## Setup Instructions

### 1. Spotify API Access

To obtain Spotify API access:

1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in.
2. Click on `Create an App`.
3. Fill in the necessary details and create your application.
4. Once the application is created, you'll be provided with a `Client ID` and `Client Secret`.

### 2. Configure the Script

1. Clone or download this repository.
2. Open the script in a text editor.
3. Update the following placeholders with the appropriate values:
   - `SPOTIFY_CLIENT_ID`: Your Spotify Client ID.
   - `SPOTIFY_CLIENT_SECRET`: Your Spotify Client Secret.
   - `LIDARR_API_URL`: The API URL for your Lidarr installation.
   - `LIDARR_API_KEY`: Your Lidarr API key.

### 3. Run the Script

With everything set up, you can run the script. It will:

1. Fetch missing tracks and albums from Lidarr.
2. Search for them on Spotify.
3. Save their Spotify URLs to separate files (`spotify_tracks.txt` for tracks and `spotify_albums.txt` for albums).
4. Use `d-fi` to download these tracks and albums.

```bash
pip install requests
python lidarr-defi.py
```
### 4. Optional
You can set this script to run at regular intervals (e.g., daily or weekly) to automatically fetch and download the latest missing tracks and albums from Lidarr.

### Contribution
Feel free to fork this repository and make improvements or adapt it to better suit your needs. If you make substantial improvements, consider making a pull request to help enhance the functionality for all users.

### Disclaimer
Please note that downloading copyrighted music without the proper permissions may be illegal in your country. Use this script responsibly and ensure you have the rights to the music you download.
