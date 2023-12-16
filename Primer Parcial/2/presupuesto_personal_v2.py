import psycopg2
from datetime import date

def conectar_db():
    try:
        conexion = psycopg2.connect(
            database="presupuesto_personal",
            user="postgres",
            password="proyectos",
            host="localhost",
            port="5432"
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except psycopg2.Error as e:
        print("Error de conexión:", e)
        raise

def cerrar_conexion(conexion):
    if conexion:
        conexion.close()
        print("Conexión cerrada.")

def crear_tabla_tipos_gastos(conexion):
    with conexion.cursor() as cursor:
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tipos_gastos (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL
                );
            """)
            # Verificar si la restricción ya existe antes de agregarla
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.constraint_column_usage
                    WHERE table_name = 'tipos_gastos'
                        AND constraint_name = 'tipos_gastos_nombre_key'
                );
            """)
            if not cursor.fetchone()[0]:
                cursor.execute("""
                    ALTER TABLE tipos_gastos
                    ADD CONSTRAINT tipos_gastos_nombre_key UNIQUE (nombre);
                """)
            conexion.commit()
        except psycopg2.Error as e:
            print("Error al crear la tabla tipos_gastos:", e)

def crear_tabla_gastos(conexion):
    with conexion.cursor() as cursor:
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gastos (
                    id SERIAL PRIMARY KEY,
                    tipo_id INTEGER REFERENCES tipos_gastos(id),
                    descripcion VARCHAR(255) NOT NULL,
                    monto NUMERIC NOT NULL,
                    fecha DATE NOT NULL
                );
            """)
            conexion.commit()
        except psycopg2.Error as e:
            print("Error al crear la tabla gastos:", e)

def crear_tabla_presupuesto(conexion):
    with conexion.cursor() as cursor:
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS presupuesto (
                    id SERIAL PRIMARY KEY,
                    tipo_id INTEGER REFERENCES tipos_gastos(id) UNIQUE,
                    monto_presupuestado NUMERIC NOT NULL
                );
            """)
            conexion.commit()
        except psycopg2.Error as e:
            print("Error al crear la tabla presupuesto:", e)

def ingresar_gasto(conexion):
    tipo_gasto = input("Ingrese el tipo de gasto: ")
    descripcion = input("Ingrese la descripción del gasto: ")
    monto = float(input("Ingrese el monto del gasto: "))
    fecha = date.today()

    with conexion.cursor() as cursor:
        try:
            cursor.execute("BEGIN;")

            # Insertar el tipo de gasto (si no existe)
            cursor.execute("INSERT INTO tipos_gastos (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING RETURNING id;", (tipo_gasto,))
            tipo_id_result = cursor.fetchone()
            tipo_id = tipo_id_result[0] if tipo_id_result else None

            # Insertar el gasto en la tabla gastos
            cursor.execute("INSERT INTO gastos (tipo_id, descripcion, monto, fecha) VALUES (%s, %s, %s, %s);", (tipo_id, descripcion, monto, fecha))

            cursor.execute("COMMIT;")
            print("Gasto ingresado correctamente.")
        except psycopg2.Error as e:
            print("Error al ingresar el gasto:", e)
            cursor.execute("ROLLBACK;")

def ver_resumen_gastos(conexion):
    with conexion.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT tipos_gastos.nombre, SUM(gastos.monto) AS total_gastado
                FROM gastos
                JOIN tipos_gastos ON gastos.tipo_id = tipos_gastos.id
                GROUP BY tipos_gastos.nombre
                ORDER BY total_gastado DESC;
            """)
            resultados = cursor.fetchall()

            if resultados:
                print("\nResumen de Gastos Acumulados:")
                for resultado in resultados:
                    print(f"{resultado[0]}: Q{resultado[1]:,.2f}")
            else:
                print("No hay gastos registrados.")
        except psycopg2.Error as e:
            print("Error al obtener el resumen de gastos:", e)

def ajustar_presupuesto(conexion):
    tipo_gasto = input("Ingrese el tipo de gasto para ajustar el presupuesto: ")
    monto_presupuestado = float(input("Ingrese el nuevo monto presupuestado: "))

    with conexion.cursor() as cursor:
        try:
            cursor.execute("BEGIN;")

            # Insertar el tipo de gasto (si no existe)
            cursor.execute("INSERT INTO tipos_gastos (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING RETURNING id;", (tipo_gasto,))
            tipo_id_result = cursor.fetchone()

            if tipo_id_result is not None:
                tipo_id = tipo_id_result[0]
            else:
                # Si el tipo de gasto ya existe, obtenemos su ID
                cursor.execute("SELECT id FROM tipos_gastos WHERE nombre = %s;", (tipo_gasto,))
                tipo_id_result = cursor.fetchone()

                if tipo_id_result is not None:
                    tipo_id = tipo_id_result[0]
                else:
                    print("Error: No se pudo obtener el tipo de gasto.")
                    raise psycopg2.Error("Error: No se pudo obtener el tipo de gasto.")

            # Resto del código para ajustar el presupuesto
            cursor.execute("UPDATE presupuesto SET monto_presupuestado = %s WHERE tipo_id = %s;", (monto_presupuestado, tipo_id))

            cursor.execute("COMMIT;")
            print("Presupuesto ajustado correctamente.")
        except psycopg2.Error as e:
            print("Error al ajustar el presupuesto:", e)
            cursor.execute("ROLLBACK;")

def mostrar_menu():
    print("\nMenú:")
    print("1. Ingresar un gasto")
    print("2. Ver resumen de gastos")
    print("3. Ajustar presupuesto")
    print("0. Salir")

def main():
    conexion = conectar_db()
    crear_tabla_tipos_gastos(conexion)
    crear_tabla_gastos(conexion)
    crear_tabla_presupuesto(conexion)

    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de la opción (0-3): ")

        if opcion == "1":
            ingresar_gasto(conexion)
        elif opcion == "2":
            ver_resumen_gastos(conexion)
        elif opcion == "3":
            ajustar_presupuesto(conexion)
        elif opcion == "0":
            cerrar_conexion(conexion)
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()
