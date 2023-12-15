import psycopg2
import matplotlib.pyplot as plt
import numpy as np

def conectar_db():
    try:
        conexion = psycopg2.connect(
            database="analisis_financiero",
            user="postgres",
            password="proyectos",
            host="localhost",
            port="5432"
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except Exception as e:
        print("Error de conexión:", e)
        return None

def agregar_columnas_empresas(conexion):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                ALTER TABLE empresas
                ADD COLUMN IF NOT EXISTS costo_acumulado NUMERIC,
                ADD COLUMN IF NOT EXISTS utilidad_acumulada NUMERIC;
            """)
            conexion.commit()
            print("Columnas 'costo_acumulado' y 'utilidad_acumulada' agregadas correctamente a la tabla empresas.")
    except Exception as e:
        print("Error al agregar las columnas:", e)

def ingresar_empresa(conexion):
    try:
        with conexion.cursor() as cursor:
            nombre = input("Ingrese el nombre de la empresa: ")
            ventas_acumuladas = float(input("Ingrese las ventas acumuladas: "))
            costo_acumulado = float(input("Ingrese el costo acumulado: "))
            utilidad_acumulada = float(input("Ingrese la utilidad acumulada:"))

            cursor.execute("""
                INSERT INTO empresas (nombre, ventas_acumuladas, costo_acumulado, utilidad_acumulada)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (nombre, ventas_acumuladas, costo_acumulado, utilidad_acumulada))

            empresa_id = cursor.fetchone()[0]
            print(f"Empresa {nombre} ingresada con ID: {empresa_id}")
        conexion.commit()
    except Exception as e:
        print("Error al ingresar la empresa:", e)

def seleccionar_empresa(conexion):
    try:
        with conexion.cursor() as cursor:
            empresa = input("Ingrese el nombre de la empresa: ")
            cursor.execute("SELECT * FROM empresas WHERE nombre = %s;", (empresa,))
            resultado = cursor.fetchone()
            if resultado:
                print("ID:", resultado[0])
                print("Nombre:", resultado[1])
                print("Ventas acumuladas:", resultado[2])
                print("Costo acumulado:", resultado[3])
                print("Utilidad acumulada:", resultado[4])
            else:
                print("No se encontró ninguna empresa con ese nombre.")
        conexion.commit()
    except Exception as e:
        print("Error al seleccionar la empresa:", e)

def ver_grafico(conexion, empresa_id):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT EXTRACT(YEAR FROM CURRENT_DATE) AS anio,
                       SUM(ventas_acumuladas) AS total_ventas,
                       SUM(costo_acumulado) AS total_costo,
                       SUM(utilidad_acumulada) AS total_utilidad
                FROM empresas
                WHERE id = %s
                GROUP BY anio
                ORDER BY anio;
            """, (empresa_id,))
            
            resultados = cursor.fetchall()

            if resultados:
                anios = np.array([resultado[0] for resultado in resultados])
                total_ventas = np.array([resultado[1] for resultado in resultados])
                total_costo = np.array([resultado[2] for resultado in resultados])
                total_utilidad = np.array([resultado[3] for resultado in resultados])

                # Realizar una correlación lineal entre ventas y utilidad acumulada
                correlacion_lineal = np.corrcoef(total_ventas.astype(float), total_utilidad.astype(float))[0, 1]
                print(f"La correlación lineal entre ventas y utilidad acumulada es: {correlacion_lineal}")

                # Generar un gráfico de barras
                plt.bar(anios, total_ventas, label='Ventas')
                plt.bar(anios, total_costo, label='Costo', alpha=0.5)
                plt.bar(anios, total_utilidad, label='Utilidad', alpha=0.5)

                plt.xlabel('Año')
                plt.ylabel('Montos')
                plt.title('Análisis Financiero por Año')
                plt.legend()
                plt.show()
            else:
                print("No hay datos para mostrar.")

        conexion.commit()
        print("Generando gráfico...")
    except Exception as e:
        print("Error al generar el gráfico:", e)

def ver_tabla(conexion):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM empresas;")
            resultados = cursor.fetchall()
            for resultado in resultados:
                print("ID:", resultado[0])
                print("Nombre:", resultado[1])
                print("Ventas acumuladas:", resultado[2])
                print("Costo acumulado:", resultado[3])
                print("Utilidad acumulada:", resultado[4])
        conexion.commit()
    except Exception as e:
        print("Error al mostrar la tabla:", e)

def main():
    conexion = conectar_db()
    if conexion:
        agregar_columnas_empresas(conexion)  # Asegurarse de tener las columnas en la tabla empresas
        while True:
            print("\n1. Ingresar datos de una nueva empresa")
            print("2. Seleccionar empresa para análisis")
            print("3. Ver resultados en gráfico")
            print("4. Ver resultados en tabla")
            print("5. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion.isdigit():
                opcion = int(opcion)
                if opcion == 1:
                    ingresar_empresa(conexion)
                elif opcion == 2:
                    seleccionar_empresa(conexion)
                elif opcion == 3:
                    empresa_id = input("Ingrese el ID de la empresa para el análisis: ")
                    ver_grafico(conexion, empresa_id)
                elif opcion == 4:
                    ver_tabla(conexion)
                elif opcion == 5:
                    print("Saliendo del programa...")
                    break
                else:
                    print("Opción no válida.")
            else:
                print("Por favor, ingrese un número.")
        
        conexion.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
