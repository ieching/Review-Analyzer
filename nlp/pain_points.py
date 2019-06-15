from sklearn.feature_extraction.text import CountVectorizer
from vader import get_sentiment
from preprocess import process_text
import pandas as pd

def get_frequent(corpus, n=None):
	# gets the top n words that appear from the corpus

	# converts corpus into a Bag of Words
	bow_transformer = CountVectorizer(max_features = 1000).fit(corpus)
	bow = bow_transformer.transform(corpus)

	# finds the most frequent words
	sum_words = bow.sum(axis=0)
	words_freq = [(word, sum_words[0, idx]) for word, idx in bow_transformer.vocabulary_.items()]

	# sorts words in descending frequency
	words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)

	# returns a list of tuples with format (word, frequency)
	return words_freq[:n]

def get_tokens(list_of_tuples):
    # returns a list of the tokens from the list of tuples of most frequent words
    tokens = [word for word, freq in list_of_tuples]
    return tokens

def token_sentence_matcher(token, text):
    # checks if the token is found in the sentence (returns true if found)
    for word in text.split():
        if word == token:
            return True
    return False

def create_token_column(token, dataframe, matcher_col_name):
    # creates a column that contains a boolean for whether the token is found
    dataframe[token] = dataframe[matcher_col_name].apply(lambda x: token_sentence_matcher(token, x))

def create_token_match_columns(token_list, dataframe):
    # creates columns for each token in the list of tokens to search for
    for i in range(0,len(token_list)):
        create_token_column(token_list[i], dataframe, 'review_tokens')

def get_negative_tokens(list_of_tuples):
	# returns a list of tokens with negative sentiment
	neg_corp = [word for word, freq in list_of_tuples if (get_sentiment(word) < 0)]
	return neg_corp

def check_contain_tokens(list_of_tokens, text):
	# check if a text contains any tokens from the list of tokens
	sentences = text.split('.')
	for sentence in sentences:
		words = sentence.split()
		for word in words:
			for token in list_of_tokens:
				if (word == token):
					return True
	return False

def get_sentence(token, text):
	# gets the sentence in which the token appears in
	sentences = text.split('.')
	for sentence in sentences:
		words = sentence.split()
		for word in words:
			if (word == token):
				return sentence
	return None

def check_neg_sentence(text):
	# checks if a sentence has a negative sentiment
 	if text != None:
	 	if (get_sentiment(text) < 0):
	 		return True
 	return False

def get_neg_sentence(token, text):
	# gets the sentence in which the token appears in only if the processed sentence is negative
	sentences = text.split('.')
	for sentence in sentences:
		words = sentence.split()
		for word in words:
			if (process_text(word) == token and get_sentiment(process_text(sentence)) < 0 and get_sentiment(sentence) < 0):
				return sentence
	return None

def process_token_df(neg_token_list, dataframe):
	# creates dataframes for each token in the corpus and removes empty values before concatenating the dataframes
    token_df_list = []
    
    for index in range(0, len(neg_token_list)):
        token_df = dataframe[dataframe[neg_token_list[index]]]
        token_df['neg_sentence'] = token_df['review_content'].apply(lambda x: get_neg_sentence(neg_token_list[index], x))
        token_df.dropna(inplace=True)
        token_df['df_len'] = len(token_df)
        token_df['token'] = neg_token_list[index]

        if len(token_df != 0):
            token_df_list.append(token_df)
    
    new_df = pd.concat(token_df_list)
    new_df.reset_index(inplace=True)
    return new_df