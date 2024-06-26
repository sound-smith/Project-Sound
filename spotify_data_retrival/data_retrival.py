import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import dotenv
from typing import Dict, List
import json
import math
import time
import os

# output directory (change this to song_data/{your name})
OUTPUT_DIRECTORY: str = "Chris"
OUTPUT_DIRECTORY: str = os.path.join("song_data", OUTPUT_DIRECTORY)
# put playlsit url below
PLAYLIST_URL: str = (
    "https://open.spotify.com/playlist/37i9dQZF1EIgNoWOvbnUCk?si=e50decd2070d4620"
)
# put the name of the playlist here in snake(_) cas
PLAYLIST_NAME: str = "Happy Mix"
# default number of songs, will change.
PLAYLIST_NUMBER_OF_SONGS: int = 0

# CONSTANTS
PLAYLIST_FILE_PATH = os.path.join(OUTPUT_DIRECTORY, f"{PLAYLIST_NAME}_ids.json")
TRACK_DETAILS_FILE_PATH = os.path.join(
    OUTPUT_DIRECTORY, f"{PLAYLIST_NAME}_track_details.json"
)


def main():
    """
    This function sets up the Spotify API credentials and calls the other functions to get the playlist tracks and track details.
    """
    # load the .env file with the Spotify API credentials
    # create '.env' file in spotifyDataRetrival directory
    # add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to .env file
    # Ex: 
    # SPOTIFY_CLIENT_ID={your client id}
    # SPOTIFY_CLIENT_SECRET = {your client secret}
    dotenv.load_dotenv(".env")

    # Set up Spotify API credentials
    client_id = dotenv.dotenv_values().get("SPOTIFY_CLIENT_ID")
    client_secret = dotenv.dotenv_values().get("SPOTIFY_CLIENT_SECRET")
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # create output directory
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    # get playlist tracks
    get_playlist_tracks(PLAYLIST_URL, sp, PLAYLIST_FILE_PATH)
    # get song list and ids
    song_list = read_json(PLAYLIST_FILE_PATH)
    # get track details
    track_details = get_track_details(song_list, sp)
    write_json(TRACK_DETAILS_FILE_PATH, track_details)


def read_json(file_name: str) -> List[Dict[str, str]]:
    """read CSV file as a dictionary

    Args:
        file_name (str): File name and location to read.

    Returns:
        List[Dict[str, str]]: List of Songs in dictionary format.
    """
    song_list: List[Dict[str, str]] = []
    with open(os.path.join(os.getcwd(), file_name), "r", encoding="utf-8") as file:
        song_list = json.load(file)
    return song_list


def get_playlist_tracks(playlist_url: str, sp: spotipy.Spotify, playlist_file_path: str) -> None:
    """
    gets playlist tracks and writes to a file

    Args:
        playlist_url (str): URL to the playlist.
        sp (spotipy.Spotify): Spotify object to use, must be authenticated.
        playlist_file_path (str): File path to write to.
        playlist_name (str, optional): Name of the playlist.
    """
    playlist = sp.playlist_tracks(playlist_url)
    PLAYLIST_NUMBER_OF_SONGS = playlist["total"]
    if PLAYLIST_NUMBER_OF_SONGS < 100:
        offset = 1
    else:
        offset = math.ceil(PLAYLIST_NUMBER_OF_SONGS / 100)
    tracks: List[Dict[str, str]] = []

    # Get playlist tracks in 100s
    for i in range(0, offset):
        all_songs = sp.playlist_tracks(playlist_url, offset=i * 100)
        PLAYLIST_NUMBER_OF_SONGS = all_songs["total"]
        for track in all_songs["items"]:
            tracks.append(
                {
                    "track_id": track["track"]["id"],
                    "track_name": track["track"]["name"],
                    "artist_name": track["track"]["artists"][0]["name"],
                    "album_name": track["track"]["album"]["name"],
                }
            )
        time.sleep(2.5)  # sleep for 2.5 seconds to not overload spotify api

        # Write tracks to CSV file
        with open(
            os.path.join(os.getcwd(), playlist_file_path), "w", encoding="utf-8"
        ) as file:
            writer = json.dumps(tracks)
            file.write(writer)


def get_track_details(tracks: List[Dict[str, str]], sp: spotipy.Spotify) -> List[Dict[str, str]]:
    """
    gets track details and returns a dictionary

    Args:
        tracks (List[Dict[str, str]]): Track details to fetch
        sp (spotipy.Spotify): Authenticated Spotify object
    Returns:
        List[Dict[str, str]]: A list of dictionaries containing track details
    """
    track_details = []
    # Divide tracks into smaller subsets for Spotify API processing
    chunk_size = 100
    track_subsets = [tracks[i:i+chunk_size] for i in range(0, len(tracks), chunk_size)]

    for track_subset in track_subsets:
        track_ids = [track["track_id"] for track in track_subset]
        
        try:
            # Fetch audio features from Spotify API
            audio_features = sp.audio_features(track_ids)
        except Exception as e:
            print(f"Error fetching audio features: {e}")
            continue
        
        for index, track_feature in enumerate(audio_features):
            if track_feature is None:
                # Skip tracks with missing audio features
                continue
            
            # Construct track details dictionary
            track_detail = {
                "track_id": track_subset[index]["track_id"],
                "track_name": track_subset[index]["track_name"],
                "artist_name": track_subset[index]["artist_name"],
                "album_name": track_subset[index]["album_name"],
                # Add audio features to the track details
                **track_feature
            }
            track_details.append(track_detail)
        
        # Pause before making the next request to avoid rate limiting
        time.sleep(2.5)
    
    return track_details

def write_json(file_name: str, track_details: List[Dict[str, str]]) -> None:
    """
    Writes a dictionary of track details to a CSV file.

    Args:
        file_name (str): The name of the CSV file to write to.
        track_details (Dict[str, Dict[str, str]]): A dictionary of track details, where the key is a string of the form
            '{track name} - {artist name} - {album name}', and the value is a dictionary of audio features.
    """
    with open(os.path.join(os.getcwd(), file_name), "w", encoding="utf-8") as file:
        writer = json.dumps(track_details)
        file.write(writer)


if __name__ == "__main__":
    main()
