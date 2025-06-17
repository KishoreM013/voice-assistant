import speech_recognition as sr

recognize  = sr.Recognizer()

with sr.Microphone() as source:
    try:
        speech = recognize.listen(source)
        text = recognize.recognize_google(speech)
        print(text)
    except:
        print('Something is happend')
