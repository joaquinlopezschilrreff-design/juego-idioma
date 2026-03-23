import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

duration = 5  
sample_rate = 44100

print("Habla ahora...")
recording = sd.rec(
  int(duration * sample_rate), # el número de muestras a grabar
  samplerate=sample_rate,      # tasa de muestreo
  channels=1,                  # 1 significa grabación mono
  dtype="int16")               # tipo de datos para las muestras grabadas
sd.wait()  # esperando a que termine la grabación

wav.write("output.wav", sample_rate, recording)
print("Grabación completa, ahora reconociendo...")


recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="es")
        print("Dijiste:", text)
        
    except sr.UnknownValueError:             
        print("No se pudo reconocer el habla.")

    except sr.RequestError as e:       
        print(f"Error del servicio: {e}")

idiomas = {
"Inglés": "en",
"Español": "es",
"Ruso": "ru",
"Portugués": "pt",
"Indonesio": "id",
"Polaco": "pl",
"Italiano": "it",
"Turco": "tr "
}

lang = input(f"¿Que idioma quieres traducir tu texto? {idiomas}")
        

translator = Translator()
translated = translator.translate(text, dest=lang)  
print("🌍 Traducción al ", lang , translated.text)
