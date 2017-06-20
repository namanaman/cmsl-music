import feature_extractor as fe
from sklearn.cross_validation import cross_val_score
from sklearn.naive_bayes import GaussianNB
import csv

'''Important Notes:
    use "python -m nltk.downloader all" t download all the NLTK data
    the cfig file in each function corresponds to the extract_features function in fe
'''

def decade_features():
    '''Extracts features from the 2006-2015 lyrics dataset'''
    infile = "datasets/lyrics_10Year.csv"
    lyric_dict = {}
    lyrics = []
    cfig = ['lem', 'plex']

    f = open(infile, 'rt')
    reader = csv.reader(f)
    for r in reader:
        lyric_dict[(r[0], r[1])] = r[3] #title, artist:lyrics
    for key in lyric_dict:
        lyrics.append(lyric_dict[key])

    features, header = fe.extract_features(lyrics, cfig)
    f2 = open("datasets/nltk_10Year.csv", 'w')
    f2.write('title,' + 'artist,' + ','.join(header) + '\n')
    for song, row in zip(lyric_dict.keys(), features):
        str_row = [str(i) for i in row]
        f2.write(song[0] + ',' + song[1] + ',' + ','.join(str_row) + '\n')

    f.close()
    f2.close()

    return features

def generic_features(infile, outfile):
    '''Extracts features from any lyric dataset in the format of (title, artist, lyrics, label)'''
    lyric_dict = {}
    lyrics = []
    labels = []
    cfig = ['lem', 'plex']

    f = open(infile, 'rt', encoding="utf8")
    reader = csv.reader(f)
    for r in reader:
        lyric_dict[(r[0], r[1], r[3])] = r[2] #title, artist, label:lyrics
    for key in lyric_dict:
        lyrics.append(lyric_dict[key])
        labels.append(key[2])

    features, header = fe.extract_features(lyrics, cfig)
    f2 = open(outfile, 'w', encoding="utf8")
    f2.write('title,' + 'artist,' + ','.join(header) + ',' + 'popular' + '\n')
    for song, row in zip(lyric_dict.keys(), features):
        str_row = [str(i) for i in row]
        f2.write(song[0] + ',' + song[1] + ',' + ','.join(str_row) + ',' + song[2] + '\n')

    f.close()
    f2.close()

    return features, labels

def predict_popularity(X, Y):
    scores = cross_val_score(GaussianNB(), X, Y, scoring='accuracy', cv=10)
    return scores.mean()

if __name__ == "__main__":
    '''create csv files for features and print prediction accuracies'''
    decade_features()
    all_, ah= generic_features("datasets/lyrics_10Week.csv", "datasets/nltk_all.csv")
    coldplay_, ch = generic_features("datasets/lyrics_coldplay.csv", "datasets/nltk_coldplay.csv")
    drake_, dh = generic_features("datasets/lyrics_drake.csv", "datasets/nltk_drake.csv")
    rihanna_, rh = generic_features("datasets/lyrics_rihanna.csv", "datasets/nltk_rihanna.csv")

    print("last 10 weeks prediction: ", predict_popularity(all_,ah))
    print("coldplay prediction: ", predict_popularity(coldplay_,ch))
    print("rihanna prediction: ", predict_popularity(rihanna_,rh))
    print("drake prediction: ", predict_popularity(drake_,dh))