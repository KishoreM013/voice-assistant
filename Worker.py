from time import sleep

from Engine import Engine
from Compiler import Compiler

from pygame import mixer 

import pandas as pd 

from speech_recognition import Recognizer
from speech_recognition import Microphone

import pyttsx3 as Speaker 
import nltk 

nltk.download('words')
english_words = set(nltk.corpus.words.words())

engine = Engine()
compiler = Compiler()
speaker = Speaker.init()
mixer.init() 

speaker.setProperty('rate', 100)
speaker.setProperty('volume', 0.8)

def load_embeddings():
    embedds = pd.read_csv('embeddings.csv')
    embedds = embedds.T
    print('Reload finished')
    return 

embedds = pd.read_csv('embeddings.csv')
embedds = embedds.T
print(embedds)

read_audio = Recognizer()

while True: 
    with Microphone() as source:
        print('Say my name.....')
        speaker.say('Say my name')
        speaker.runAndWait()
        audio = read_audio.listen(source)

        try:
            text = read_audio.recognize_google(audio, language= 'en-US')
            text = str(text) 
            print('You are Goddamn right')
            speaker.say('You are god damn right')
            speaker.runAndWait()
            if text.lower() == 'bye':
                break 
            text = compiler.load(text)
            sleep(2)

        except Exception as e:
            print(e)


print('Bye, See you soon')
speaker.say('Its not an end, just a break. See you soon')
