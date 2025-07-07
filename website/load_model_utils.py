# load_model_utils.py
import os
import requests
import gzip
import shutil
from fasttext import load_model

model_path = 'cc.cy.300.bin'
gz_path = 'cc.cy.300.bin.gz'
url = 'https://huggingface.co/drelhaj/fasttext-welsh/resolve/main/cc.cy.300.bin.gz'

def get_model():
    if not os.path.isfile(model_path):
        try:
            print("Downloading Welsh FastText model...")
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(gz_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            with gzip.open(gz_path, 'rb') as f_in:
                with open(model_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(gz_path)
            print("Model downloaded and ready.")
        except Exception as e:
            print(f"Error downloading model: {e}")
            return None

    try:
        return load_model(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
