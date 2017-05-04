# cmsl-music
Lexically analyzing lyrics of songs to predict their popularity

## Problem 1
How do the lexical features of a song’s lyrics predict its popularity?
Based on last 10 weeks of Billboard Hot 100 singles and corresponding unpopular songs

## Problem 2
How have the lexical features of a Top 100 song’s lyrics changed in the past decade?
Based on last 10 years of Billboard Year-End Hot 100 Single found on https://github.com/walkerkq/musiclyrics

## Problem 3 
For popular artists like Drake and Rihanna, is there a significant difference in lexical content of their popular vs. unpopular songs? 
A related question would be if a model can accurately classify if an artist’s song is popular or unpopular based on certain lexical features.

## Extracting NLTK features
- run 'python driver.py'
- to change which features (from feature_extractor.py) are evaluated, change the 'cfig' array in the feature extractor functions of driver.py
- driver.py will produce csv files containing feature counts for the corpora corresponding to each of the three above problems; it will also print out cross validation scores for problems one and three