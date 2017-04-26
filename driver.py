import feature_extractor as fe
import csv

'''Important Notes:
    use "python -m nltk.downloader all" t download all the NLTK data
    the cfig file in each function corresponds to the extract_features function in fe
'''

def decade_features():
    '''Extracts features from the 2006-2015 lyrics dataset'''
    infile = "datasets/decade_lyrics.csv"
    lyric_dict = {}
    lyrics = []
    cfig = ['fw', 'syn', 'lex', 'punct', 'plex']

    f = open(infile, 'rt')
    reader = csv.reader(f)
    for r in reader:
        lyric_dict[(r[0], r[1])] = r[3] #title, artist:lyrics
    for key in lyric_dict:
        lyrics.append(lyric_dict[key])

    features, header = fe.extract_features(lyrics, cfig)
    f2 = open("datasets/nltk_decade.csv", 'w')
    f2.write('title,' + 'artist,' + ','.join(header) + '\n')
    for song, row in zip(lyric_dict.keys(), features):
        str_row = [str(i) for i in row]
        f2.write(song[0] + ',' + song[1] + ',' + ','.join(str_row) + '\n')

    f.close()
    f2.close()

def generic_features(infile, outfile):
    '''Extracts features from any lyric dataset in the format of (title, artist, lyrics, label)'''
    lyric_dict = {}
    lyrics = []
    cfig = ['syn', 'lex', 'plex']

    f = open(infile, 'rt', encoding="utf8")
    reader = csv.reader(f)
    for r in reader:
        lyric_dict[(r[0], r[1], r[3])] = r[2] #title, artist, label:lyrics
    for key in lyric_dict:
        lyrics.append(lyric_dict[key])

    features, header = fe.extract_features(lyrics, cfig)
    f2 = open(outfile, 'w', encoding="utf8")
    f2.write('title,' + 'artist,' + ','.join(header) + ',' + 'popular' + '\n')
    for song, row in zip(lyric_dict.keys(), features):
        str_row = [str(i) for i in row]
        f2.write(song[0] + ',' + song[1] + ',' + ','.join(str_row) + ',' + song[2] + '\n')

    f.close()
    f2.close()

decade_features()
generic_features("datasets/all_lyrics.csv", "datasets/nltk_all.csv")
generic_features("datasets/coldplay_lyrics.csv", "datasets/nltk_coldplay.csv")
generic_features("datasets/drake_lyrics.csv", "datasets/drake_all.csv")
generic_features("datasets/rihanna_lyrics.csv", "datasets/rihanna_all.csv")