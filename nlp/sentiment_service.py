import requests
import json

def use_sentiment_service(text):
	# returns 0 if negative, 1 if neutral, and 2 if positive
	words_array = text.split()
	response = requests.request(method='get', url='http://localhost:9500/predict', json={"words_array":words_array})
	json_response = json.loads(response.text)

	value = max(json_response['prediction'])
	if value < 0.4:
		i = 1;
	else:
		i = json_response['prediction'].index(value)
	
	return i

def get_full_sentiment(text):
	words_array = text.split()
	response = requests.request(method='get', url='http://localhost:9500/predict', json={"words_array":words_array})
	json_response = json.loads(response.text)
	
	return json_response