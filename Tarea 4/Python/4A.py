import numpy as np
import matplotlib.pyplot as plt

# Definir el vector de tiempo t
t = np.arange(-0.04, 0.041, 0.001)

# Calcular la señal exponencial compleja x
x = 20 * np.exp(1j * (80 * np.pi * t - 0.4 * np.pi))

# Crear el primer subgráfico 3D
fig = plt.figure(figsize=(10, 6))

ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.plot3D(t, np.real(x), np.imag(x))
ax1.grid()
ax1.set_title('20*e^{j*(80*pi*t-0.4*pi)}')
ax1.set_xlabel('Tiempo, s')
ax1.set_ylabel('Real')
ax1.set_zlabel('Imag')

# Crear el segundo subgráfico con dos líneas
ax2 = fig.add_subplot(2, 1, 2)
ax2.plot(t, np.real(x), 'b', label='Real')
ax2.plot(t, np.imag(x), 'r', label='Imaginario')
ax2.grid()
ax2.set_title('Rojo - Componente Imaginario, Azul - Componente Real de la Exponencial')
ax2.set_xlabel('Tiempo')
ax2.set_ylabel('Amplitud')
ax2.legend()

# Mostrar los gráficos
plt.show()
