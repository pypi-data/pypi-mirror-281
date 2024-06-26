from keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Load the model and tokenizer
model = load_model('BiLSTM.h5')

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


# Function to predict the lemma
def predict_lemma(word):
    
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
