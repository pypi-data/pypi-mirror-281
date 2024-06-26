# emotion_detection/main.py
import sys

import pandas as pd
import tensorflow as tf
from preprocessing import clean_text 
from model import build_model, train_model, evaluate_model, predict_emotion
from utils import *
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
import keras
import pickle
import os
'''
# Load dataset
df = pd.read_csv('text.csv')

# Preprocess data
df = df.drop('Number', axis=1)
label_encoder = LabelEncoder()
df['label_encoded'] = label_encoder.fit_transform(df['label'])
# Manually create the label mapping
label_mapping = dict(zip(label_encoder.inverse_transform(df['label_encoded']), df['label_encoded']))
df=df.drop('label',axis=1)
df=df.rename(columns={'label_encoded':'label'})

unique_review = df['text'].unique()


df['cleaned_text'] = df['text'].apply(clean_text)

df['cleaned_text'] = df['cleaned_text'].str.replace("http", "").str.replace("href", "").str.replace("img", "").str.replace("irc", "")

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(df['cleaned_text'], df['label'], test_size=0.3, random_state=42)

# Tokenize text data

tokenizer = Tokenizer(num_words=50000)

tokenizer.fit_on_texts(X_train)
with open('tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

X_train_padded = pad_sequences(tokenizer.texts_to_sequences(X_train), maxlen=100, padding='post')
X_test_padded = pad_sequences(tokenizer.texts_to_sequences(X_test), maxlen=100, padding='post')

# Build and train model
mymodel = build_model(input_dim=50000, output_dim=len(label_encoder.classes_))
myhistory = train_model(mymodel, X_train_padded, y_train, X_test_padded, y_test, epochs=50)

#saving
model_json = mymodel.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
mymodel.save_weights("model.weights.h5")
#-----------


# Evaluate model
loss, accuracy = evaluate_model(mymodel, X_test_padded, y_test)
print(f'Test Loss: {loss}')
print(f'Test Accuracy: {accuracy}')
'''
#load




json_file2 = open('model2.json', 'r')
loaded_model_json2 = json_file2.read()
json_file2.close()
loaded_model2 = model_from_json(loaded_model_json2)
# load weights into new model
loaded_model2.load_weights("model2.weights.h5")







label_map={'fear': 1, 'sad': 4, 'love': 3, 'joy': 2, 'surprise': 5, 'anger': 0}
# Predict example
example_text = input('Enter a text to find the emotion:\n')
#predicted_emotion = predict_emotion(mymodel, tokenizer, example_text,label_map)
#predicted_emotion1 = predict_emotion(loaded_model, tokenizer, example_text,label_map)
predicted_emotion2 = predict_emotion(loaded_model2,  example_text,label_map)

#print(f'Predicted Emotion for "{example_text}": {predicted_emotion1}')
print(f'Predicted Emotion for "{example_text}": {predicted_emotion2}')


'''
# Visualize results (optional)
# Confusion matrix

# Classification report

y_pred = np.argmax(mymodel.predict(X_test_padded), axis=1)
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))


plot_confusion_matrix(y_pred, y_test, label_encoder.classes_)
plt.show()
# Plot training history
history_of(myhistory)
'''
