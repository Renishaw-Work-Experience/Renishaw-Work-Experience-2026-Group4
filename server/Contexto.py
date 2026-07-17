"""
type
HINT
TERMINATE
RANK

the word may be a number
most moels describe meaning rather than common contexts
"""

# Ensure SSL verification uses the certifi CA bundle (helps on Windows environments)
import os
import certifi
import ssl
from math import ceil

# Set environment variables and default SSL context to use certifi's CA bundle
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
try:
    # Make sure the default HTTPS context is a callable that returns a certifi-backed context
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
except Exception:
    # If this fails, we'll still try to proceed and provide helpful error messages
    pass

import gensim.downloader as api
from random import choice, randint
import sys

model_name = "glove-wiki-gigaword-50"
limit = 10000

def main(word=None):
    saved_fname = model_name + ".kv"

    # Try loading from a previously saved KeyedVectors file first
    wv = None
    if os.path.exists(saved_fname):
        try:
            from gensim.models import KeyedVectors
            wv = KeyedVectors.load(saved_fname, mmap="r")
            print(f"Loaded KeyedVectors from {saved_fname}")
        except Exception as e:
            print(f"Failed to load saved KeyedVectors ({saved_fname}): {e}. Falling back to downloader.", file=sys.stderr)
            wv = None

    # If no saved file or load failed: try downloader
    if wv is None:
        try:
            loaded = api.load(model_name)
            print(f"Downloaded object type: {type(loaded)}")
        except Exception as e:
            print(f"Failed to load '{model_name}' from downloader: {e}", file=sys.stderr)
            return 1

        # If the downloader returned KeyedVectors, use it directly
        if hasattr(loaded, "index_to_key"):
            wv = loaded
        else:
            # Try to train a Word2Vec model from the dataset (e.g., 'text8' returns sentences)
            try:
                from gensim.models import Word2Vec
                print("Dataset is not KeyedVectors — attempting to train Word2Vec on it")
                model = Word2Vec(loaded, vector_size=100, window=5, min_count=5, workers=1)
                wv = model.wv
                print("Trained Word2Vec and obtained KeyedVectors (model.wv)")
            except Exception as e:
                print(f"Failed to train Word2Vec on the dataset: {e}", file=sys.stderr)
                # As a last resort, try to use the loaded object directly
                wv = loaded

    # Optionally save a copy for faster reloads later (only if not already saved)
    if not os.path.exists(saved_fname):
        try:
            if hasattr(wv, "save"):
                wv.save(saved_fname)
                print(f"Saved KeyedVectors to {saved_fname}")
            else:
                print("Loaded object has no .save; cannot save KeyedVectors.", file=sys.stderr)
        except Exception as e:
            print(f"Warning: could not save KeyedVectors locally: {e}", file=sys.stderr)

    vocab_words = list(wv.index_to_key)

    if word is None:
        word = choice(vocab_words[0:5000])
        #word = str(randint(0,200))
        #word = "password"
        #print(f"Using random seed word: {word}")
    similar = wv.most_similar(word, topn=20000)
    similar_list = [i[0]for i in similar]
    #print(word)
    """
    print(f"Top similar words to '{word}':")
    count = 0
    for w, score in similar:
        count +=1
        print(f"{w}: {score:.4f}")
        if count>10:
            break"""
    guesses = []
    hint_count = 0
    
    


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(main(arg))