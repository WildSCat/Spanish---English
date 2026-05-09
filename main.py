import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

translations_by_level = {
    "facil": {
        "gato": "cat",
        "perro": "dog",
        "manzana": "apple",
        "leche": "milk",
        "sol": "sun"
    },
    "medio": {
        "banano": "banana",
        "escuela": "school",
        "amigo": "friend",
        "ventana": "window",
        "amarillo": "yellow"
    },
    "dificil": {
        "tecnologia": "technology",
        "universidad": "university",
        "informacion": "information",
        "pronunciacion": "pronunciation",
        "imaginacion": "imagination"
    }
}


def grabar_audio(filename="output.wav", duration=5, sample_rate=44100):
    print("Grabando... habla ahora.")
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    wav.write(filename, sample_rate, recording)
    print(f"Grabación completa: {filename}")
    return filename


def reconocer_desde_archivo(filename="output.wav", language="es-ES"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    try:
        texto = recognizer.recognize_google(audio, language=language)
        print(f"Texto reconocido: {texto}")
        return texto.strip().lower()
    except sr.UnknownValueError:
        print("No se pudo reconocer el habla en el archivo.")
        return None
    except sr.RequestError as e:
        print(f"Error del servicio de reconocimiento: {e}")
        return None
    except Exception as e:
        print(f"Error al leer el archivo de audio: {e}")
        return None


def traducir_texto(texto, src="es", dest="en"):
    try:
        translator = Translator()
        resultado = translator.translate(texto, src=src, dest=dest)
        return resultado.text.lower()
    except Exception as e:
        print(f"Error al traducir el texto: {e}")
        return None


def reconocer_traduccion():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando... Di la palabra en inglés:")
        try:
            audio = recognizer.listen(source, timeout=6)
            texto = recognizer.recognize_google(audio, language="en-US")
            print(f"Dijiste: {texto}")
            return texto.strip().lower()
        except sr.UnknownValueError:
            print("No entendí lo que dijiste.")
            return None
        except sr.RequestError as e:
            print(f"Error al conectar con el servicio de reconocimiento: {e}")
            return None
        except Exception as e:
            print(f"Error al capturar audio: {e}")
            return None


def juego_traduccion():
    print("¡Bienvenido al juego de traducción español->inglés!")
    nivel = input("Selecciona un nivel (facil, medio, dificil): ").lower()

    if nivel not in translations_by_level:
        print("Nivel no válido. Por favor, selecciona facil, medio o dificil.")
        return

    palabra_es = random.choice(list(translations_by_level[nivel].keys()))
    traduccion_correcta = translations_by_level[nivel][palabra_es]
    intentos = 3

    print(f"Traduce esta palabra al inglés: {palabra_es}")

    while intentos > 0:
        traduccion_usuario = reconocer_traduccion()
        if not traduccion_usuario:
            intentos -= 1
            print(f"Intentos restantes: {intentos}")
            continue

        if traduccion_usuario == traduccion_correcta:
            print(f"¡Correcto! La traducción de '{palabra_es}' es '{traduccion_correcta}'.")
            break
        else:
            print(f"Incorrecto. Dijiste '{traduccion_usuario}'.")
            intentos -= 1
            if intentos > 0:
                print(f"Intenta otra vez. Intentos restantes: {intentos}")

    if intentos == 0:
        print(f"Se agotaron los intentos. La respuesta correcta era '{traduccion_correcta}'.")


def modo_grabacion_y_reconocimiento():
    filename = grabar_audio()
    texto = reconocer_desde_archivo(filename)
    if texto:
        print(f"Texto detectado: {texto}")
    else:
        print("No se pudo obtener texto del audio.")


def modo_grabacion_y_traduccion():
    filename = grabar_audio()
    texto = reconocer_desde_archivo(filename)
    if not texto:
        print("No se pudo obtener texto del audio.")
        return

    traduccion = traducir_texto(texto)
    if traduccion:
        print(f"Texto original: {texto}")
        print(f"Traducción al inglés: {traduccion}")
    else:
        print("No se pudo traducir el texto.")


def mostrar_banner():
    banner = r"""
  ____  _                           _     _       
 | __ )(_) ___ _ ____   _____ _ __ (_) __| | ___  
 |  _ \| |/ _ \ '_ \ \ / / _ \ '_ \| |/ _` |/ _ \ 
 | |_) | |  __/ | | \ V /  __/ | | | | (_| | (_) |
 |____/|_|\___|_| |_|\_/ \___|_| |_|_|\__,_|\___/ 
                                                  

      Juego de traducción español -> inglés
"""
    print(banner)


def main():
    while True:
        mostrar_banner()
        print("1. Juego: español -> inglés usando voz")
        print("2. Grabar audio y reconocer texto en español")
        print("3. Grabar audio, reconocer español y traducir a inglés")
        print("4. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            juego_traduccion()
        elif opcion == "2":
            modo_grabacion_y_reconocimiento()
        elif opcion == "3":
            modo_grabacion_y_traduccion()
        elif opcion == "4":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()

