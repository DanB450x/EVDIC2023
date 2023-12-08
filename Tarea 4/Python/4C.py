import numpy as np
import matplotlib.pyplot as plt

# Crear el vector n
n = np.arange(-50, 51)

# Calcular las señales x, y, z
x = np.cos(np.pi * 0.1 * n)
y = np.cos(np.pi * 0.9 * n)
z = np.cos(np.pi * 2.1 * n)

# Crear y mostrar los subgráficos
plt.figure(figsize=(8, 6))

plt.subplot(3, 1, 1)
plt.plot(n, x)
plt.title('$x[n]=\cos(0.1\pi n)$')
plt.grid()

plt.subplot(3, 1, 2)
plt.plot(n, y)
plt.title('$y[n]=\cos(0.9\pi n)$')
plt.grid()

plt.subplot(3, 1, 3)
plt.plot(n, z)
plt.title('$z[n]=\cos(2.1\pi n)$')
plt.xlabel('n')
plt.grid()

plt.tight_layout()
plt.show()
