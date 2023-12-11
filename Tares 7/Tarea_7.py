import psycopg2

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    dbname='IVA',
    user='postgres',
    password='proyectos',
    host='localhost',
    port='5432'
)

# Crear un cursor para ejecutar consultas
cur = conn.cursor()

# Ingreso del precio del producto
precio = float(input("Ingrese el precio de su producto: Q"))

# Cálculos relacionados con el IVA
IVA = precio * 0.12
precio_sin_iva = precio - IVA

print(f"El precio sin IVA es de Q{precio_sin_iva:.0f}, el IVA es de Q{IVA:.0f}")

try:
    # Preparar la instrucción SQL para la inserción
    Ins1 = 'INSERT INTO calculo (ptotal) VALUES (%s);'  # %s es un marcador de posición para el valor
    Instruccion = cur.mogrify(Ins1, (precio,))

    # Ejecutar la instrucción SQL
    cur.execute(Instruccion)

    # Confirmar la transacción
    conn.commit()

except psycopg2.Error as e:
    print(f"Error durante la conexión a la DB. Consulte el error: {e}")

finally:
    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()
