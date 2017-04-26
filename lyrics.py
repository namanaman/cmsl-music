# CMSL Final Project
## Reads Billboard data and gets lyrics from Genius API

import csv
import requests
import re
from bs4 import BeautifulSoup
import pickle

def getLyrics(song_api_path, headers, base_url):
    song_url = base_url + song_api_path
    r = requests.get(song_url, headers=headers).json()

    path = r["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)

    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find("lyrics").get_text()
    return lyrics

def saveData(csvData, filename):
    base_url = "http://api.genius.com"
    headers = {'Authorization': 'Bearer TOKEN'} #TOKEN replaced by actual
    search_url = base_url + "/search"

    lyricData = []
    for i in range(len(csvData)):
        data = {'q': csvData[i][1]}
        r = requests.get(search_url, params=data, headers=headers).json()

        song_info = None
        for hit in r["response"]["hits"]:
            if hit["result"]["primary_artist"]["name"].lower() == csvData[i][0].lower():
                song_info = hit
                break

        if song_info:
            song_api_path = song_info["result"]["api_path"]
            lyrics = getLyrics(song_api_path, headers, base_url)
            lyricData.append([csvData[i][1], csvData[i][0], lyrics, csvData[i][2]])

    print(len(lyricData))
    with open(filename, 'w', newline='') as f:
        a = csv.writer(f, delimiter=',')
        a.writerows(lyricData)

def getArtistData():
    with open('Popular-v-Unpopular.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

    drakeData = data[:113]
    rihannaData = data[113:197]
    coldplayData = data[197:]

    saveData(drakeData, 'drakeData.csv')
    saveData(rihannaData, 'rihannaData.csv')
    saveData(coldplayData, 'coldplayData.csv')

def getSongData():
    with open('updated_Hot100Data.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

    for i in range(len(data)):
        split_artists = re.split(' x | Featuring ', data[i][1])
        data[i][1] = split_artists[0]

    saveData(data, 'popularLyrics.csv')

def combineCSV():
    with open('popularExtraSongs.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

    with open(r'popularLyrics.csv', 'a') as f:
        writer = csv.writer(f)
        for song in data:
            writer.writerow([song[0], song[1], song[2], lyrics])

def cleanData():
    with open('final/drakeData.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

    for song in data:
        lyrics = song[3]
        lyrics2 = lyrics.replace('\r', ' ').replace('\n', ' ')
        lyrics3 = ' '.join(lyrics2.split())
        song[3] = re.sub("[\(\[].*?[\)\]]", "", lyrics3)

    with open('clean_drakeData.csv', 'w', newline='') as f:
        a = csv.writer(f, delimiter=',')
        a.writerows(data)

if __name__ == "__main__":
    with open('coldplayData.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

    for song in data:
        lyrics = song[2]
        lyrics2 = lyrics.replace('\r', ' ').replace('\n', ' ')
        lyrics3 = ' '.join(lyrics2.split())
        song[2] = re.sub("[\(\[].*?[\)\]]", "", lyrics3)

    with open('final_coldplayData.csv', 'w', newline='') as f:
        a = csv.writer(f, delimiter=',')
        a.writerows(data)
