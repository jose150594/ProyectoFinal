import csv
import pandas as pd

# Lista para almacenar datos
datos = []

# Función para guardar los datos en un archivo CSV
def guardar_en_csv():
    with open("estudiantes.csv", mode="w", newline="") as archivo:
        escritor = csv.writer(archivo)
        # Escribe encabezados
        escritor.writerow(["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (cm)", "IMC", "Presión Sistólica", "Presión Diastólica"])
        # Escribe los datos
        for usuario in datos:
            escritor.writerow(usuario)
    print("Archivo CSV generado exitosamente.")

# Función para cargar los datos desde un archivo CSV
def cargar_desde_csv():
    global datos
    try:
        with open("estudiantes.csv", mode="r") as archivo:
            lector = csv.reader(archivo)
            next(lector)  # Salta el encabezado
            datos = [list(map(lambda x: int(x) if x.isdigit() else x, fila)) for fila in lector]
        print("Datos cargados exitosamente desde el archivo CSV.")
    except FileNotFoundError:
        print("Archivo CSV no encontrado. Se iniciará una nueva lista.")

# Función para registrar los datos biomédicos
def datos_biomedicos():
    numero_de_identificacion = int(input("Ingrese su número de identificación: "))
    nombre = str(input("Ingrese nombres y apellidos: "))
    edad = int(input("Ingrese su edad: "))
    peso = float(input("Ingrese su peso (kg): "))
    estatura = float(input("Ingrese su estatura (cm): "))
    imc = (peso / (estatura / 100) ** 2)
    usuario = [numero_de_identificacion, nombre, edad, peso, estatura, imc, None, None]
    datos.append(usuario)
    print("Datos registrados exitosamente.")

# Función principal
def principal():
    cargar_desde_csv()  # Cargar datos al iniciar
    while True:
        print("\n1. Registro de estudiante")
        print("2. Buscar estudiante según el número de identificación")
        print("3. Monitorear presión arterial de estudiante")
        print("4. Mostrar datos en DataFrame")
        print("5. Mostrar estudiante con IMC mínimo y máximo")
        print("6. Generar archivo CSV")
        print("7. Cargar datos desde archivo CSV e imprimirlos")
        print("8. Salir del programa")

        seleccion = input("Escriba su elección: ")

        if seleccion == "1":
            datos_biomedicos()
        elif seleccion == "2":
            numero_de_identificacion = int(input("Ingrese el número de identificación: "))
            busqueda(numero_de_identificacion)
        elif seleccion == "3":
            numero_de_identificacion = int(input("Ingrese el número de identificación: "))
            monitoreo_presion(numero_de_identificacion)
        elif seleccion == "4":
            mostrar_datos_dataframe()
        elif seleccion == "5":
            mostrar_imc_min_max()
        elif seleccion == "6":
            guardar_en_csv()
        elif seleccion == "7":
            cargar_desde_csv()
            mostrar_datos_dataframe()
        elif seleccion == "8":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Función para mostrar los datos en un DataFrame
def mostrar_datos_dataframe():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (cm)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        print(df)
    else:
        print("No hay datos registrados.")

# Función para buscar estudiante con IMC mínimo y máximo
def mostrar_imc_min_max():
    try:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (cm)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        min_imc = df.loc[df["IMC"].idxmin()]
        max_imc = df.loc[df["IMC"].idxmax()]
        print("\nEstudiante con IMC mínimo:")
        print(min_imc)
        print("\nEstudiante con IMC máximo:")
        print(max_imc)
    except ValueError:
        print("No hay suficientes datos para calcular el IMC mínimo y máximo.")

# Función de búsqueda
def busqueda(numero_de_identificacion):
    for usuario in datos:
        if usuario[0] == numero_de_identificacion:
            print(f"Estudiante encontrado: {usuario}")
            return
    print("Estudiante no registrado.")

# Función para monitorear la presión arterial
def monitoreo_presion(numero_de_identificacion):
    for usuario in datos:
        if usuario[0] == numero_de_identificacion:
            presion_sistolica = int(input("Ingrese su presión sistólica: "))
            presion_diastolica = int(input("Ingrese su presión diastólica: "))
            usuario[6] = presion_sistolica
            usuario[7] = presion_diastolica
            guardar_en_csv()  # Actualizar CSV
            if presion_sistolica < 120 and presion_diastolica < 80:
                print("Presión normal.")
            elif 120 <= presion_sistolica < 140 or 80 <= presion_diastolica < 90:
                print("Advertencia: Presión alta.")
            elif presion_sistolica >= 140 or presion_diastolica >= 90:
                print("Advertencia: Hipertensión.")
            return
    print("Estudiante no registrado.")

# Ejecutar programa principal
principal()


