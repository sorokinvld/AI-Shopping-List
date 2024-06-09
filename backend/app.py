
# importing required libraies
from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import spacy                        # scacy is used for nlp

app = Flask(__name__)
CORS(app)                           # Enable CORS, to allow cross-origin requests (access resources from other domain)

# Initializing the spaCy language model, to perform different nlp tasks 
nlp = spacy.load("en_core_web_sm")                              # en_core_web_sm is a pre-trained English language model

@app.route("/abc", methods=["POST"])                            # defining route, POST method used to fetch the data
def transcribe_audio():                                         #defining the function "transcribe_audio"
    if "audio" not in request.files:                            #logical part
        return jsonify({"error": "No audio file found"}), 400   # if the above line is true, it reurns the error message

    audio_file = request.files["audio"]                         # retrieves the uploaded audio 
    transcribed_text = transcribe_audio_file(audio_file)        # passes the audio_file to the function
    shopping_list = extract_shopping_list(transcribed_text)     # Variable to store the shopping list

    return jsonify({"transcribedText": transcribed_text, "shoppingList": shopping_list})    # returns the JSON response containg the transcibed text and the shopping list

def transcribe_audio_file(audio_file):                          # defining function
    recognizer = sr.Recognizer()                                # initializes speech recognizer
    audio_data = sr.AudioFile(audio_file)                       # Variable holds the audio file
    with audio_data as source:                                  # utilizes the recognizer
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def extract_shopping_list(transcribed_text):
    doc = nlp(transcribed_text)                                         # result of applying the spaCy pipeline to the transcribed_text
    shopping_list = {}
    for token in doc:                                                   # for loop
        if token.pos_ == "NOUN" and token.head.pos_ == "NUM":           # checking noun and num for item name and quantity
            shopping_list[token.text.lower()] = int(token.head.text)    # if above condition fulfilled, it will extract item name and quantity
    return shopping_list                                                # returns the value of the shopping_list

if __name__ == "__main__":                              
    app.run(debug=True)
