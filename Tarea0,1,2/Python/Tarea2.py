import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
fs = 1000  # Frecuencia de muestreo en Hz
t = np.arange(0, 1, 1/fs)  # Vector de tiempo de 1 segundo

# Señal senoidal 1
A1 = 1
f1 = 100
S1 = A1 * np.sin(2 * np.pi * f1 * t)

# Señal senoidal 2
A2 = 0.8
f2 = 300
S2 = A2 * np.sin(2 * np.pi * f2 * t)

# Generando ruido aleatorio con media de cero
med = 0
desv = 0.2  # Ajuste según la cantidad de ruido deseado
R = desv * np.random.randn(len(t)) + med

# Generando señal compuesta con ruido
S_Comp = S1 + S2 + R

# Calculando la Transformada Discreta de Fourier utilizando fft
TDF = np.fft.fft(S_Comp)

# Calcular el eje de frecuencia correspondiente
f = np.arange(0, fs, fs/len(TDF))

# Señal generada en el dominio del tiempo
plt.subplot(2, 1, 1)
plt.plot(t, S_Comp)
plt.title('Señal Compuesta con Ruido')
plt.xlabel('Tiempo[s]')
plt.ylabel('Amplitud')

# Gráfica de TDF en el dominio de la frecuencia
plt.subplot(2, 1, 2)
plt.plot(f, np.abs(TDF))
plt.title('Transformada Discreta de Fourier (TDF)')
plt.xlabel('Frecuencia[Hz]')
plt.ylabel('Magnitud')

# Ajustar los límites del eje x en la segunda subtrama para mostrar solo frecuencias positivas
plt.xlim([0, fs/2])

plt.show()
