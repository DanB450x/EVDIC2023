import math

def calcular_factorial():
    try:
        # Pedir al usuario que ingrese un número
        numero = int(input('Ingrese un número para calcular su factorial: '))

        # Verificar si el número es un entero no negativo
        if numero >= 0:
            # Calcular el factorial del número
            resultado = math.factorial(numero)
            print(f'El factorial de {numero} es {resultado}')
        else:
            # Mostrar un mensaje si el número no es un entero no negativo
            print('No se puede calcular el factorial. Ingrese un entero no negativo.')
    except ValueError:
        # Manejar el caso en el que el usuario ingresa algo que no es un número entero
        print('Error: Ingrese un número entero.')

# Llamar a la función
calcular_factorial()
