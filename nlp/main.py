# general
import numpy as np
import pandas as pd
import os
import datetime

# processing
from preprocess import filter_pos, process_text, remove_nt
from vader import get_sentiment
from pain_points import get_frequent, get_negative_tokens, create_token_match_columns, process_token_df

# database
from pymongo import MongoClient
from pycommon.warehouse.load_queries import acquire_all_review_data
from pycommon.warehouse.store_insights import store_painpoint_insights
from pycommon.warehouse.objects import painpoint_object

# getting data from database
# port = os.getenv("MONGO_PORT") if os.getenv("MONGO_PORT") is not None else 27017 # MONGO_PORT defines the port number. 
port= 27017
mongo_client = MongoClient('localhost', port) # mongo is always the host. Again, docker handles this dns resolution.

# And we're good! mongo is ready to be used. Most of the methods in pycommon/warehouse need you to 
# pass in the mongoclient. 

reviews = acquire_all_review_data(
        mongo_client, 
        datetime.datetime(2001,12,1,0,0).timestamp(), # from
        datetime.datetime(2018,12,1,0,0).timestamp(), # to
        "SimpangAsia",
        "Yelp"
    )

reviews_array = []
for review in reviews:
    reviews_array.append(review)

# converting into dataframe
d = {
    "timestamp": [reviews_array[i].timestamp for i in range(0,len(reviews_array))],
    "source_id": [reviews_array[i].source_id for i in range(0,len(reviews_array))],
    "business_id": [reviews_array[i].business_id for i in range(0,len(reviews_array))],
    "review_id": [reviews_array[i].review_id for i in range(0,len(reviews_array))],
    "review_content": [reviews_array[i].content for i in range(0,len(reviews_array))],
    "review_rating": [reviews_array[i].rating for i in range(0,len(reviews_array))],
}

df = pd.DataFrame(data=d)

# processes dataframe
# retains only adjectives and adverbs for reviews
df['review_tokens'] = df['review_content'].apply(filter_pos)
# Makes lowercase, removes punctuation and stopwords, and lemmatizes remaining words
df['review_tokens'] = df['review_tokens'].apply(process_text)
# removes the word 'nt'
df['review_tokens'] = df['review_tokens'].apply(remove_nt)

# getting tokens
most_freq = get_frequent(df['review_tokens'],500)
neg_corp = get_negative_tokens(most_freq)

# creating dataframe columns for processing purposes
create_token_match_columns(neg_corp, df)
token_df = process_token_df(neg_corp, df)

# sorting the dataframe in terms of length (most evidence)
token_df.sort_values(['df_len','token'], ascending = False, inplace=True)
token_df.reset_index(inplace=True)

# moving the processed data into the dataframe
# ALL NEGATIVE TOKENS AND THEIR EVIDENCE WILL BE ADDED TO THE DATAFRAME; NOT JUST THE TOP 10 NEGATIVE TOKENS
final_tokens = list(pd.unique(token_df['token']))
# list of painpoint_object objects
all_objects = []

for token in final_tokens:
    review_id_evidence = {}
    
    review_ids = token_df[token_df['token'] == token]['review_id']
    for review_id in review_ids:

        evidence = list(token_df[(token_df['review_id'] == review_id) & (token_df['token'] == token)]['neg_sentence'])
        review_id_evidence[review_id] = evidence
    
    # creates a painpoint_object object
    pain_point = painpoint_object(token, "Description", "Solution", "Yelp", "SimpangAsia", review_id_evidence, datetime.datetime(2018,12,1,0,0).timestamp())
    all_objects.append(pain_point)
    
# adding to the db and checking if successful
store_success = store_painpoint_insights(mongo_client, all_objects)
if store_success:
    print("yay its done")
else:
    print("riperdoodles")