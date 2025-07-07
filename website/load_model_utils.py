# load_model_utils.py
import os
import requests
from fasttext import load_model

model_path = 'cc.cy.300.bin'
url = 'https://huggingface.co/drelhaj/fasttext-welsh/resolve/main/cc.cy.300.bin'

def get_model():
    if not os.path.isfile(model_path):
        try:
            print("Downloading Welsh FastText model...")
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(model_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print("Model downloaded and ready.")
        except Exception as e:
            print(f"Error downloading model: {e}")
            return None

    try:
        return load_model(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
