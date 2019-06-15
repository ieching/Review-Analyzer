import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_sentiment(text):
    # gets the compound score of the sentiment using the VADER lexicon
    sid = SentimentIntensityAnalyzer()
    
    results = sid.polarity_scores(text)
    sentiment = results['compound']
    return sentiment