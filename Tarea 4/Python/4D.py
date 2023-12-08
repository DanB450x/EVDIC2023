import numpy as np
import matplotlib.pyplot as plt

# Crear el vector n
n = np.arange(-3, 8)

# Calcular la señal x
x = 0.55**(n + 3)

# Definir la señal impulso h
h = np.ones(11)

# Realizar la convolución
y = np.convolve(x, h, mode='full')

# Crear y mostrar los subgráficos
plt.figure(figsize=(8, 6))

plt.subplot(3, 1, 1)
plt.stem(n, x)
plt.title('Señal Original')
plt.grid()

plt.subplot(3, 1, 2)
plt.stem(n, h)
plt.title('Respuesta al impulso / Segunda señal')
plt.grid()

plt.subplot(3, 1, 3)
plt.stem(np.arange(len(y)), y)
plt.title('Convolución restante')
plt.grid()

plt.tight_layout()
plt.show()
