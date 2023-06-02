##Command line
##curl "http://127.0.0.1:5000/api/synonyms?word=pobl"

###Python Use
import requests
import json


response = requests.get('http://127.0.0.1:5000/api/synonyms', params={'word': 'pobl'})
data = response.json()

print(json.dumps(data, indent=2))
