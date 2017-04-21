# CMSL Final Project
## Reads Billboard data and gets lyrics from Genius API

import csv
import requests
import re
from bs4 import BeautifulSoup

def readCSV():
    filename = 'BillboardHot100Data.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

    for i in range(len(data)):
        split_artists = re.split(' x | Featuring ', data[i][1])
        data[i][1] = split_artists[0]

    return data

def getLyrics(song_api_path, headers, base_url):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()

    path = json["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)

    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find("lyrics").get_text()
    return lyrics

if __name__ == "__main__":
    base_url = "http://api.genius.com"
    headers = {'Authorization': 'Bearer TOKEN'} #TOKEN replaced by actual
    search_url = base_url + "/search"
    csvData = readCSV()
    songs = len(csvData)
    for i in range(songs):
        data = {'q': csvData[i][0]}
        response = requests.get(search_url, params=data, headers=headers)
        json = response.json()

        song_info = None
        for hit in json["response"]["hits"]:
            if hit["result"]["primary_artist"]["name"].lower() == csvData[i][1].lower():
                song_info = hit
                break

        if song_info:
            count = count + 1
            song_api_path = song_info["result"]["api_path"]
            getLyrics(song_api_path, headers, base_url)
