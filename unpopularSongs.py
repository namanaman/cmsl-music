import csv
import requests
import base64
import pickle

#Gets unpopular songs from same album for 10-Week Corpus

def readCSV():
    filename = 'billboardSongSpotifyID.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    data = [val for sublist in data for val in sublist] #Flatten list
    return data

def getAlbumInfo(songID, token):
    song_url = 'https://api.spotify.com/v1/tracks/' + songID
    r = requests.get(song_url, headers={'Authorization': token}).json()

    albumType = r['album']['album_type']
    if albumType == 'album':
        album_url = 'https://api.spotify.com/v1/albums/' + r['album']['id']
        album_response = requests.get(album_url, headers={'Authorization': token})
        album_json = album_response.json()
        album_popularity = album_json['popularity']

        trackIDs = []
        for track in album_json['tracks']['items']:
            trackIDs.append(track['id'])

        stringIDs = ','.join(trackIDs)
        track_url = 'https://api.spotify.com/v1/tracks/'
        track_response = requests.get(track_url, params={'ids': stringIDs}, headers={'Authorization': token}).json()
        for track in track_response['tracks']:
            trackName = track['name']
            popularity = track['popularity']
            if popularity + 10 < album_popularity:
                break

        return r['name'], trackName, r['artists'][0]['name']

def getUnpopular():
    token = 'Bearer TOKEN'
    songIDs = readCSV()

    pkl_file = open('Unpopular.pkl', 'rb')
    unpopular_songs = pickle.load(pkl_file)

    for song in songIDs:
        pair = getAlbumInfo(song, token)
        if pair:
            original, unpopular, artist = pair
            unpopular_songs[original] = (unpopular, artist)

    return unpopular_songs

if __name__ == "__main__":
    #unpop = getUnpopular()
    #with open('Unpopular.pkl', 'wb') as f:
        #pickle.dump(unpop, f, pickle.HIGHEST_PROTOCOL)

    pkl_file = open('Unpopular.pkl', 'rb')
    unpopular_songs = pickle.load(pkl_file)
    print(len(unpopular_songs.keys()))
