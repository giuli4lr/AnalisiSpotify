import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import streamlit as st
from collections import Counter

# Configurazione Spotipy
CLIENT_ID = "240892898a1b45e68a641a9aeab8011b"
CLIENT_SECRET = "e53fb3bc73db47e1897037c415d2df28"
REDIRECT_URI = "http://127.0.0.1:5000"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read"
    )
)

# Titolo
st.markdown("<h1 style='color: #32a852;'>Analisi dei miei brani Spotify 🎵</h1>", unsafe_allow_html=True)

# Spaziatura
st.write("")
st.write("")

# Brani più ascoltati
st.markdown("<h2 style='color: #ff6347;'>Brani più ascoltati</h2>", unsafe_allow_html=True)
options = {
    "Ultimo mese": "short_term",
    "Ultimi 6 mesi": "medium_term",
    "Di sempre": "long_term"
}

# Widget radio per la selezione
selected_option = st.radio("Seleziona il periodo di tempo:", options.keys())

# Recupera il valore dell'API corrispondente
time_range = options[selected_option]

# Recupera i dati limita 25
top_tracks = sp.current_user_top_tracks(limit=25, time_range=time_range)

# Mostra i risultati
for idx, track in enumerate(top_tracks['items'], start=1):
    st.write(f"{idx}. {track['name']} di {track['artists'][0]['name']}")

# Spaziatura
st.write("")
st.write("")

# Grafico della popolarità dei brani
st.markdown("<h2 style='color: #e8c743;'>Grafico della Popolarità dei Brani</h2>", unsafe_allow_html=True)

st.write("Visualizza i brani da te più ascoltati e il loro punteggio di popolarità globale.")

max_characters = 25
track_names = [
    track['name'][:max_characters] + '...' if len(track['name']) > max_characters else track['name']
    for track in top_tracks['items']
]
track_popularity = [track['popularity'] for track in top_tracks['items']]

fig, ax = plt.subplots()
bars = ax.barh(track_names, track_popularity, color='skyblue')
ax.set_title("Popolarità dei Brani")
ax.invert_yaxis()

# Aggiungi i valori all'interno delle barre
for bar, popularity in zip(bars, track_popularity):
    ax.annotate(f'{popularity}', xy=(popularity, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0), textcoords="offset points", va='center', ha='left')

st.pyplot(fig)

st.write("")
st.write("")

# Recupera generi per gli artisti dei brani della top 25
st.markdown("<h2 style='color: #7da832;'>I generi più ascoltati</h2>", unsafe_allow_html=True)

genres = []
for track in top_tracks['items']:
    artist_id = track['artists'][0]['id']
    artist = sp.artist(artist_id)
    genres.extend(artist['genres'])

genre_counts = Counter(genres)
# Visualizza i generi
st.bar_chart(genre_counts)


# Artisti più ascoltati
st.subheader("")
st.markdown("<h2 style='color: #1ea6d4;'>Popolarità dei miei artisti più ascoltati</h2>", unsafe_allow_html=True)

top_artists = sp.current_user_top_artists(limit=25, time_range='short_term')
for idx, artist in enumerate(top_artists['items'], start=1):
    st.write(f"{idx}. {artist['name']} - Popolarità: {artist['popularity']}")