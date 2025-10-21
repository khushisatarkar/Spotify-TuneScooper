import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import io

SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""

st.title("🎵 Spotify TuneScooper")

playlist_url = st.text_input("Enter Spotify playlist link: ")

if playlist_url:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET
        ))

        # extract playlist id from link
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        results = sp.playlist_items(playlist_id, additional_types=['track'])

        songs = []
        while results:
            for item in results['items']:
                track = item['track']
                if track:
                    name = track['name']
                    artists = ", ".join([artist['name'] for artist in track['artists']])
                    songs.append(f"{name} - {artists}")
            if results['next']:
                results = sp.next(results)
            else:
                break

        if songs:
            st.success(f"✅ Found {len(songs)} songs!")
            
            # show songs in a text editor
            song_text = "\n".join(songs)
            st.text_area("Songs in playlist:", song_text, height=300)

            # Prepare for download
            buffer = io.BytesIO(song_text.encode("utf-8"))
            st.download_button(
                label="📥 Download as .txt",
                data=buffer,
                file_name="playlist_songs.txt",
                mime="text/plain"
            )
        else:
            st.warning("No songs found in this playlist.")

    except Exception as e:
        st.error(f"Error: {e}")
