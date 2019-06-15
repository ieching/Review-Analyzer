# libraries for preprocessing
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
import string
from pattern.en import lemma

# libraries for POS tagging and identification
import spacy
nlp = spacy.load('en_core_web_sm')

# to convert adverbs to adjectives
from itertools import chain
from nltk.corpus import wordnet as wn
from difflib import get_close_matches as gcm

def lemma_pattern(word):
	return lemma(word)

def lemmatize_word(word):
	wnl = WordNetLemmatizer()
	return wnl.lemmatize(word)

def process_text(text):
	# returns the lowercase
	text = text.lower()

	# removes punctuation
	nopunc = [char for char in text if char not in string.punctuation]
	nopunc = ''.join(nopunc)

	# removes stopwords and lemmatizes remaining words; also gets the infinitive form of the verb; converts adv to adj (sadly -> sad)
	wnl = WordNetLemmatizer()
	cleaned = [lemmatize_word(adv_to_adj(lemma(word))) for word in nopunc.split() if not word in set(stopwords.words('english'))]
	cleaned = ' '.join(cleaned)

	return cleaned

def filter_pos(text):
	# this function retains adjectives and adverbs
	doc = nlp(text)
	words = [token.text for token in doc if (token.pos_ == 'ADJ' or token.pos_ == 'ADV')]
	return ' '.join(words)

def remove_nt(text):
	# this function removes the word 'nt'
	cleaned = [word for word in text.split() if (word != 'nt')]
	return ' '.join(cleaned)

def convert_rating(text):
	# this function converts a string rating to int
	return int(text.split()[0].split('.')[0])

def adv_to_adj(word):
	possible_adj = []
	for ss in wn.synsets(word):
	  for lemmas in ss.lemmas(): # all possible lemmas
	      for ps in lemmas.pertainyms(): # all possible pertainyms
	          possible_adj.append(ps.name())
	if len(possible_adj) > 0:
		return possible_adj[0]
	return word
