# extract features from sets of lyrics using NLTK; based off of code from HW1 Feature Extractor

from nltk.corpus import stopwords
from nltk.util import ngrams
from collections import Counter
import nltk
import re
import numpy as np
import operator

def function_words(texts):
	bow = []
	header = stopwords.words('english')
	for text in texts:	#get stopwords counts for each text
		counts = []
		tokens = nltk.word_tokenize(text)
		for sw in stopwords.words('english'):
			sw_count = tokens.count(sw)
			normed = sw_count/float(len(tokens))
			counts.append(normed)
		bow.append(counts)
	bow_np = np.array(bow).astype(float)
	return bow_np, header	

def syntax(texts):
	'''
	Returns a len(texts) x 10 array with counts of 10 parts of speech for each text,
	AND the corresponding header.
	'''

	sw = stopwords.words('english')
	common_pos_tags = ['NN', 'NNP', 'DT', 'IN', 'JJ', 'NNS','CC','PRP','VB','VBG']
	punc = ['.', ',', ':', ';', '-', '\'', '\"', '(', ')','!', '?', 's', 't']

	syntax_mx = np.zeros((len(texts), 10)) #initialize features to 0

	for t, text in enumerate(texts): #iterate through texts
		tokens = nltk.word_tokenize(text)
		tokens = list(filter(lambda x: x not in sw, tokens))
		tokens = list(filter(lambda x: x not in punc, tokens))
		tags = nltk.pos_tag(tokens)
		for f, pos in enumerate(common_pos_tags): #count pos tags
			for tag in tags:
				if pos in tag:
					syntax_mx[t][f] += 1

	return syntax_mx, common_pos_tags

def lexical(texts):
	'''
	Returns a len(texts) x 30 array with counts of the most common 30 unigrams
	across all texts, AND the corresponding header.
	'''

	lexical_mx = np.zeros((len(texts), 30)) #initialize counts to zero
	mega_lexicon = [] #stores all tokens for all texts
	
	sw = stopwords.words('english')
	punc = ['.', ',', ':', ';', '-', '\'', '\"', '(', ')','!', '?', 's', 't']

	for text in texts: #remove stopwords and punctuation
		tokens = nltk.word_tokenize(text)
		tokens = list(filter(lambda x: x not in sw, tokens))
		tokens = list(filter(lambda x: x not in punc, tokens))

		mega_lexicon.extend(tokens) #add all tokens to lexicon

	#obtain most common 30 unigrams and sort into list
	unigrams = Counter(mega_lexicon).most_common(30)
	sorted_unigrams = sorted(unigrams, key=operator.itemgetter(1), reverse=True)

	for t, text in enumerate(texts): #count unigrams for each text
		tokens = nltk.word_tokenize(text)
		tokens = list(filter(lambda x: x not in sw, tokens))
		tokens = list(filter(lambda x: x not in punc, tokens))
		for u, gram in enumerate([x[0] for x in sorted_unigrams]):
			if len(tokens) == 0: #temp fix
				lexical_mx[t][u] += 0
			else:
				lexical_mx[t][u] += tokens.count(gram)/float(len(tokens)) #store normed unigram counts

	header = [x[0] for x in sorted_unigrams]

	return lexical_mx, header
		
		
def punctuation(texts):
	'''
	Returns a len(texts) x 10 array with counts of the 10 punctuation marks
	for each text, as well as the corresponding header.
	'''

	punct_array = ['.', ',', ':', ';', '-', '\'', '\"', '(', '!', '?']
	header = ['period', 'comma', 'colon', 'semi-colon', 'dash', 'single quote', 'double quotes', 'left paren', 'right paren', 'question mark']

	punctuation_mx = np.zeros((len(texts), 10)) #initialize punctuation counts to zero

	for t, text in enumerate(texts): #count punctation marks per text
		tokens = nltk.word_tokenize(text)
		for p, punct in enumerate(punct_array):
			punctuation_mx[t][p] = tokens.count(punct)/len(tokens)

	return punctuation_mx, header

def complexity(texts):
	'''
	Returns a len(texts) x 4 array with counts for 4 complexity checks:
	0)average characters per word 1)count of unique words  2)average words per sentence 3)count of long words used (length >= 6)
	across all texts, AND the corresponding header.
	'''

	header = ['average characters', 'uniqueness', 'average words', 'num long words']
	complexity_mx = np.zeros((len(texts), 4))

	sw = stopwords.words('english')
	punc = ['.', ',', ':', ';', '-', '\'', '\"', '(', ')','!', '?', 's', 't']

	for t, text in enumerate(texts):
		tokens = nltk.word_tokenize(text)
		tokens = list(filter(lambda x: x not in sw, tokens))

		unique_tokens = set(tokens)
		if len(tokens) != 0:
			complexity_mx[t][1] = len(unique_tokens)/len(tokens) #store uniqueness factor
		else:
			complexity_mx[t][1] = 0

		sentences = re.split('[?.!]', text)
		num_words = 0
		for sentence in sentences:
			word_list = sentence.split()
			num_words += len(word_list)
		complexity_mx[t][2] = num_words/len(sentences) #store average word counts
		
		tokens = list(filter(lambda x: x not in punc, tokens))
		num_chars = 0
		for token in tokens:
			if len(token) >= 6:
				complexity_mx[t][3] += 1 #store num long words
			num_chars += len(token)
		if len(tokens) != 0:
			complexity_mx[t][3] = complexity_mx[t][3]/len(tokens)
			complexity_mx[t][0]	= num_chars/len(tokens)	#store average character counts
		else:
			complexity_mx[t][3] = 0
			complexity_mx[t][0] = 0

	return complexity_mx, header

def extract_features(texts, conf):
	features = []
	headers = []

	if 'fw' in conf:
		f,h = function_words(texts)
		features.append(f)
		headers.extend(h)
	
	if 'syn' in conf:
		f,h = syntax(texts)
		features.append(f)
		headers.extend(h)
	
	if 'lex' in conf:
		f,h = lexical(texts)
		features.append(f)
		headers.extend(h)

	if 'punct' in conf:
		f,h = punctuation(texts)
		features.append(f)
		headers.extend(h)
	
	if 'plex' in conf:
		f,h = complexity(texts)
		features.append(f)
		headers.extend(h)

	all_features = np.concatenate(features,axis=1)

	return all_features, headers
