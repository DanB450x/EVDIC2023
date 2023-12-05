#numeros divisibles dentro de 7 y determinar el factorial
from math import factorial
import psycopg2

connection =  psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123456",
    database="proyectos",
    port="5432"
)


print("conectado a la base de datos")

a=int(input("Ingrese un número: \n"))

while True:
    try:
        if a % 7 == 0:

            connection.autocommit = True
            def insertardatos(numero, factorial):
                cursor = connection.cursor()
                query = f""" INSERT INTO factorial (numero,factorial) values('{numero}','{factorial}')"""
                cursor.execute(query)
                ursor.close()
            insertardatos(a,factorial(a))
            print("El factorial es", factorial(a))
            break
        else:
            print("no es divisible dentro de 7")
            break
    except:
        print("Ingrese un número correcto")