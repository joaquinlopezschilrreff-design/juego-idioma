import sounddevice as sd
import random
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

duration = 5  
sample_rate = 44100
max_errors = 3
score = 0
errors = 0

words = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["banana", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

level = input("Elegi el nivel de dificultad: facil, medio, dificil").strip().lower()

word_list = words[level]

random.shuffle(word_list)

translator = Translator()
recognizer = sr.Recognizer()

for word in word_list:
    print(f"Palabra:{word}")
    print("Habla ahora...")
    recording = sd.rec(
    int(duration * sample_rate), # el número de muestras a grabar
    samplerate=sample_rate,      # tasa de muestreo
    channels=1,                  # 1 significa grabación mono
    dtype="int16")               # tipo de datos para las muestras grabadas
    sd.wait()  # esperando a que termine la grabación

    wav.write("output.wav", sample_rate, recording)
    print("Grabación completa, ahora reconociendo...")
        
    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="es").lower()
            print("Dijiste:", text)
            translated = translator.translate(text, dest="en").text.lower() 
            print("🌍 Traducción al ingles" , translated)

            if text == translated:
                score += 1
                print("Sumaste 1 punto") 
            
            else: 
                errors += 1
                print(f"Sumaste 1 error ahora tenes {errors} errores")

            if errors >= max_errors:
                print("El juego termino llegaste al maximo de errores")    
                break
    except sr.UnknownValueError:
        print("No se pudo reconocer el habla.")
        errors += 1
        print(f"Sumaste 1 error ahora tenes {errors} errores")

        if errors >= max_errors:
            print("El juego termino llegaste al maximo de errores")    
            break

    except sr.RequestError as e:       
        print(f"Error del servicio: {e}")
        break


print(f"Tu puntuacion es de {score}")


