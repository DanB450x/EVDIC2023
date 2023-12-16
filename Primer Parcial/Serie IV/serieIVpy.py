import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# MENÚ
opcion = 0
while opcion != 5:
    print('Seleccione una opción')
    print('1. Grabar')
    print('2. Reproducir')
    print('3. Graficar')
    print('4. Graficar Densidad')
    print('5. Salir')

    opcion = int(input('Ingrese su elección: '))

    if opcion == 1:
        try:
            duracion = float(input('Ingrese la duración de la grabación en segundos: '))
            print('Comenzando la grabación')
            fs = 44100  # Puedes ajustar la frecuencia de muestreo según sea necesario
            datos = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype=np.int16)
            sd.wait()
            print('Grabación finalizada')
            wavfile.write('audio.wav', fs, datos)
            print('Archivo de audio grabado exitosamente')
        except:
            print('Error al grabar audio')

    elif opcion == 2:
        try:
            fs, datos = wavfile.read('audio.wav')
            sd.play(datos, fs)
            sd.wait()
        except:
            print('Error al reproducir audio')

    elif opcion == 3:
        try:
            fs, datos = wavfile.read('audio.wav')
            tiempo = np.linspace(0, len(datos) / fs, len(datos))
            plt.plot(tiempo, datos)
            plt.xlabel('Tiempo(s)')
            plt.ylabel('Amplitud')
            plt.title('Audio')
            plt.show()
        except:
            print('Error al graficar audio')

    elif opcion == 4:
        try:
            print('Graficando espectro de frecuencia')
            fs, audio = wavfile.read('audio.wav')
            f, Pxx = plt.psd(audio, NFFT=len(audio), Fs=fs)
            plt.xlabel('Frecuencia (Hz)')
            plt.ylabel('Densidad Espectral de Potencia (dB/Hz)')
            plt.title('Espectro de Frecuencia de la señal grabada')
            plt.show()
        except:
            print('Error al graficar audio')

    elif opcion == 5:
        print('Saliendo del programa')
        break

    else:
        print('Opción no válida')
