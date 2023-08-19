from flask import Blueprint, render_template, request, flash, jsonify, Flask
from flask_restful import Resource, Api
import json
import pandas as pd
import random
import re
import regex
from fasttext import load_model
import sqlite3
from flask import current_app as app
import requests
from requests.exceptions import ConnectionError
import io
import re
words = Blueprint('words',__name__)

## to get the words from the gold standard dataset 
def get_matches(word_or_synset, db):
    try:
        conn = sqlite3.connect(db)
        df = pd.read_sql_query("SELECT word, sense, synset FROM synonyms", conn)
        matches = pd.DataFrame()  # empty DataFrame for no matches

        if word_or_synset is not None:
            for index, row in df.iterrows():
                synset_string = row['synset']
                if isinstance(synset_string, str):
                    synset_list = [s.strip() for s in synset_string.split(',')]
                    if (row['word'] == word_or_synset) or (row['sense'] == word_or_synset) or (word_or_synset in synset_list):
                        new_row = {'word': row['word'], 'sense': row['sense'], 'synset': synset_list}
                        matches = pd.concat([matches, pd.DataFrame([new_row])], ignore_index=True)

            # Explode the 'synset' list into multiple rows
            matches = matches.explode(['synset'])

        if matches.empty:
            print("No matches for the word!")
        else:
            return matches

        conn.close()

    except Exception as e:
        print("An error occurred:", e)

model = load_model('./cc.cy.300.bin')
app = Flask(__name__)
api = Api(app)
class SynonymsAPI(Resource):
    def get(self):
        word = request.args.get('word', default='Thesawrws')
        synonyms = set()
        
        # Gold-standard synonyms
        gold_standard_matches= get_matches(word,'GS-synonyms.db')
        if gold_standard_matches is not None:
            gold_standard_synonyms = gold_standard_matches['synset'].tolist()
            synonyms.update(gold_standard_synonyms[:5])

        
        # Dictionary synonyms
        dictionary_matches = get_matches(word,'Dict-synonyms.db')
        if dictionary_matches is not None:
            dictionary_synonyms = dictionary_matches['synset'].tolist()
            synonyms.update(dictionary_synonyms[:5])

        # FastText synonyms
        fastText_synonyms = model.get_nearest_neighbors(word, 5)
        clean_synonyms = {syn[1] for syn in fastText_synonyms}
        synonyms.update(clean_synonyms)

        # Fine-tuned synonyms
        df = pd.read_csv("./website/data/Sk_vectors_lemma_subset.csv", index_col=False)
        fine_tuned_synonyms = df.loc[df.Gair==word]['synset'].tolist()
       
        # Select only the first five synonyms
        fine_tuned_synonyms = fine_tuned_synonyms[:5]
        synonyms.update(fine_tuned_synonyms)
        # remove the search word if it's in the synonyms set
        synonyms.discard(word)

        # remove the words that shares the same lemma with the search word 
        files = {
        'type': (None, 'rest'),
        'style': (None, 'tab'),
        'lang': (None, 'cy'),
        'text': (None, word),
        }
        # Get the lemma for the search word first
        response = requests.post('http://ucrel-api-01.lancaster.ac.uk/cgi-bin/pymusas.pl', files=files)
        word_tagged = pd.read_csv(io.StringIO(response.text), sep='\t')
        search_word_lemma = word_tagged['Lemma'][0] 
        # Get the lemmas for each synonym
        # Join all synonyms into one string

        synonyms_text = ", ".join(synonyms)

        files = {
        'type': (None, 'rest'),
        'style': (None, 'tab'),
        'lang': (None, 'cy'),
        'text': (None, synonyms_text),
            }

        response = requests.post('http://ucrel-api-01.lancaster.ac.uk/cgi-bin/pymusas.pl', files=files)

        # Read the response into a DataFrame
        synonym_tagged = pd.read_csv(io.StringIO(response.text), sep='\t')

        # Create a dictionary with synonyms as keys and lemmas as values
        synonym_lemmas = {synonym_tagged.iloc[i]["Text"]: synonym_tagged.iloc[i]["Lemma"] for i in range(len(synonym_tagged))}

        # Filter out synonyms that share the same lemma with the search word
        synonyms = {syn: lemma for syn, lemma in synonym_lemmas.items() if lemma != search_word_lemma}
        # Remove synonyms that contain numbers, punctuation, or are empty
       # synonyms = {syn.lower(): lemma for syn, lemma in synonyms.items() if re.match("^[a-zA-Z]*$", syn)and len(syn) > 1} 
        synonyms = {syn.lower(): lemma for syn, lemma in synonyms.items() if re.match("^[a-zA-Z]*$", syn) and len(syn) > 1 and is_welsh(syn.lower())}
        # Create the response dictionary
        response = {
            'word': word,
            'synonyms': list(synonyms)  
        }

        # Return the JSON response
        return jsonify(response)


###detect language
from langdetect import detect 
def is_welsh(word):
   try:
      return detect(word)== 'cy'
   except:
      return false


# Initialize the Api and add the resources
api = Api(words)
api.add_resource(SynonymsAPI, '/api/synonyms')

@words.route('/', methods=['GET', 'POST'])
def home():
    word = request.args.get('word', default='Thesawrws')

    
    #synonyms_dict = set()
    #synonyms_embed = set()
    synonyms = set()
    # Gold-standard synonyms
    gold_standard_matches= get_matches(word,'GS-synonyms.db')
    if gold_standard_matches is not None:
        gold_standard_synonyms = gold_standard_matches['synset'].tolist()
        synonyms.update(gold_standard_synonyms[:5])
    # Dictionary synonyms
    dictionary_matches = get_matches(word,'Dict-synonyms.db')
    if dictionary_matches is not None:
        dictionary_synonyms = dictionary_matches['synset'].tolist()
        synonyms.update(dictionary_synonyms[:5])

    # FastText synonyms
    fastText_synonyms = model.get_nearest_neighbors(word, 5)
    clean_synonyms = {syn[1] for syn in fastText_synonyms}
    synonyms.update(clean_synonyms)


    # Fine-tuned synonyms
    df = pd.read_csv("./website/data/Sk_vectors_lemma_subset.csv", index_col=False)
    fine_tuned_synonyms = df.loc[df.Gair==word]['synset'].tolist()
    # Select only the first five synonyms
    fine_tuned_synonyms = fine_tuned_synonyms[:5]
    synonyms.update(fine_tuned_synonyms)

    # remove the search word if it's in the synonyms set
    synonyms.discard(word)
    synonyms.discard(word)
    # remove the words that shares the same lemma with the search word 
    files = {
        'type': (None, 'rest'),
        'style': (None, 'tab'),
        'lang': (None, 'cy'),
        'text': (None, word),
    }
    # Get the lemma for the search word first
    response = requests.post('http://ucrel-api-01.lancaster.ac.uk/cgi-bin/pymusas.pl', files=files)
    word_tagged = pd.read_csv(io.StringIO(response.text), sep='\t')
    search_word_lemma = word_tagged['Lemma'][0] 
    # Get the lemmas for each synonym
    # Join all synonyms into one string

    synonyms_text = ", ".join(synonyms)

    files = {
        'type': (None, 'rest'),
        'style': (None, 'tab'),
        'lang': (None, 'cy'),
        'text': (None, synonyms_text),
            }

    response = requests.post('http://ucrel-api-01.lancaster.ac.uk/cgi-bin/pymusas.pl', files=files)

    # Read the response into a DataFrame
    synonym_tagged = pd.read_csv(io.StringIO(response.text), sep='\t')

    # Create a dictionary with synonyms as keys and lemmas as values
    synonym_lemmas = {synonym_tagged.iloc[i]["Text"]: synonym_tagged.iloc[i]["Lemma"] for i in range(len(synonym_tagged))}

    # Filter out synonyms that share the same lemma with the search word
    synonyms = {syn: lemma for syn, lemma in synonym_lemmas.items() if lemma != search_word_lemma}
    # Remove synonyms that contain numbers, punctuation, or are empty
    #synonyms = {syn.lower(): lemma for syn, lemma in synonyms.items() if re.match("^[a-zA-Z]*$", syn)and len(syn) > 1} 
    synonyms = {syn.lower(): lemma for syn, lemma in synonyms.items() if re.match("^[a-zA-Z]*$", syn) and len(syn) > 1 and is_welsh(syn.lower())}
    # Convert to DataFrame
    subset = pd.DataFrame(list(synonyms.keys()), columns=['synset'])

    # convert set to DataFrame for consistency with the rest of your code
    #subset = pd.DataFrame(list(synonyms), columns=['synset'])

    # if no synonyms found, return an informative message
    if subset.empty: 
        subset = [f"No synonyms found for the word '{word}'"]
        subset = pd.DataFrame(subset, columns=['synset'])
        #subset_dict= pd.DataFrame(synonyms_dict,columns=['synset'])

    return render_template('wordem.html', table=subset[['synset']].to_dict('records'), word=word)

def find_sentences(word, file_path, num_sentences=5):
    word_pattern = regex.compile(r'\b' + regex.escape(word.lower()) + r'\b', regex.UNICODE)
    sentences = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if word_pattern.search(line.lower()):
                sentences.append(line.strip())

    if len(sentences) > num_sentences:
        sentences = random.sample(sentences, num_sentences)
    if len(sentences) == 0:
            return ["No sentence matches found for the word."]
    return sentences


@words.route('/get_word_info', methods=['POST'])
def get_word_info():
    data = request.json
    word = data['word']
    option = data['options']
    selected_word = data['selected_word']

    df = pd.read_csv("./website/data/Fasttext_vectors_lemma_subset.csv", index_col=False)
    subset = df.loc[df.synset == selected_word]

    if not subset.empty and {'tag_1', 'lemma_1', 'pymusas_1'}.issubset(df.columns):
        tag_1 = subset.iloc[0]['tag_1']
        lemma_1 = subset.iloc[0]['lemma_1']
        pymusas_1 = subset.iloc[0]['pymusas_1']

        additional_info = f"Pos_tag: {tag_1}, Lemma: {lemma_1}, Pymusas_Tag: {pymusas_1}"
    else:
        additional_info = ""

        # Find sentences containing the word
    sentences = find_sentences(selected_word, './website/data/corcencc_clean_sentences.txt')
    sentences_html = '<br>'.join(sentences)
    


    return jsonify({'additional_info': additional_info, 'sentences': sentences_html})
