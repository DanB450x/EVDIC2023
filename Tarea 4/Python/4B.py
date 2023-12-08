import numpy as np
import matplotlib.pyplot as plt

# Crear el vector n
n = np.arange(-1000, 1001)

# Calcular la señal x
x = np.exp(1j * 2 * np.pi * 0.01 * n)

# Crear el primer subgráfico
plt.subplot(2, 1, 1)
plt.plot(n, np.real(x))
plt.title('Señal x: exp(j*2*pi*0.01*n)')
plt.xlabel('n')
plt.ylabel('Parte Real')

# Calcular la señal y
y = np.exp(1j * 2 * np.pi * 2.01 * n)

# Crear el segundo subgráfico
plt.subplot(2, 1, 2)
plt.plot(n, np.real(y), 'r')
plt.title('Señal y: exp(j*2*pi*2.01*n)')
plt.xlabel('n')
plt.ylabel('Parte Real')

# Ajustar el diseño para evitar superposiciones
plt.tight_layout()

# Mostrar los gráficos
plt.show()
