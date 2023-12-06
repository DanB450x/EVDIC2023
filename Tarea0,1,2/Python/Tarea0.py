import numpy as np
import matplotlib.pyplot as plt

# Crear un vector x de 0 a 2*pi con incrementos de 0.01
x = np.arange(0, 2*np.pi, 0.01)

# Calcular el seno de cada elemento en el vector x
y = np.sin(x)

# Graficar la función
plt.plot(x, y)
plt.title('Gráfica de y = sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
