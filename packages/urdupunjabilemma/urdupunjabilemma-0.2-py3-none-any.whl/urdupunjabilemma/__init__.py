import os
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the model and tokenizer
model_path = os.path.join(current_dir, 'BiLSTM.h5')
tokenizer_path = os.path.join(current_dir, 'tokenizer.pickle')

# Check if the model and tokenizer files exist
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")
if not os.path.exists(tokenizer_path):
    raise FileNotFoundError(f"Tokenizer file not found at: {tokenizer_path}")

model = load_model(model_path)

with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

# Function to predict the lemma
def lemmatize(word):
    max_len = 16

    # Convert the word to a sequence of integers
    sequence = tokenizer.texts_to_sequences([word])

    # Pad the sequence to the maximum length
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')

    # Predict the lemma using the trained model
    predictions = model.predict(padded_sequence)

    # Convert the prediction to the corresponding lemma
    # Since the output is a sequence, we need to take the argmax for each timestep
    lemma_sequence = np.argmax(predictions, axis=-1)[0]

    # Retrieve the corresponding lemma from the tokenizer's index_word dictionary
    lemma = ''.join([tokenizer.index_word.get(i, '') for i in lemma_sequence if i != 0])

    return lemma
