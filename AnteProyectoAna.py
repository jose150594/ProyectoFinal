import csv
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Lista para almacenar datos
datos = []

# Función para validar entrada numérica
def entrada_numerica(mensaje, tipo=float):
    while True:
        entrada = input(mensaje)
        try:
            valor = tipo(entrada)
            if valor <= 0:
                print("El valor debe ser positivo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número válido.")

# Función para guardar los datos en un archivo CSV
def guardar_en_csv():
    with open("estudiantes.csv", mode="w", newline="") as archivo:
        escritor = csv.writer(archivo)
        # Escribe encabezados
        escritor.writerow(["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"])
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
            datos = [list(map(lambda x: float(x) if x.replace('.', '').isdigit() else x, fila)) for fila in lector]
        print("Datos cargados exitosamente desde el archivo CSV.")
    except FileNotFoundError:
        print("Archivo CSV no encontrado. Se iniciará una nueva lista.")

# Función para registrar los datos biomédicos
def datos_biomedicos():
    numero_de_identificacion = entrada_numerica("Ingrese su número de identificación (solo números): ", int)
    nombre = input("Ingrese nombres y apellidos: ")
    edad = entrada_numerica("Ingrese su edad: ", int)
    peso = entrada_numerica("Ingrese su peso (kg): ")
    estatura = entrada_numerica("Ingrese su estatura en metros (ejemplo: 1.75): ")
    imc = round(peso / (estatura ** 2), 2)
    usuario = [numero_de_identificacion, nombre, edad, peso, estatura, imc, None, None]
    datos.append(usuario)
    print("Datos registrados exitosamente.")

# Submenú para análisis de datos
def submenu_analisis():
    while True:
        print("\nSubmenú de Análisis de Datos")
        print("1. Clasificar estudiantes según IMC")
        print("2. Mostrar personas con mayor y menor altura")
        print("3. Mostrar persona con mayor peso y altura")
        print("4. Volver al menú principal")

        seleccion = input("Escriba su elección: ")

        if seleccion == "1":
            clasificar_imc()
        elif seleccion == "2":
            altura_extremos()
        elif seleccion == "3":
            peso_altura_max()
        elif seleccion == "4":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Función para categorizar el IMC
def clasificar_imc():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        df['Clasificacion IMC'] = df['IMC'].apply(lambda x: "Peso insuficiente" if x < 18.5 else
                                                 "Peso normal" if x < 24.9 else
                                                 "Sobrepeso" if x < 29.9 else "Obesidad")
        print(df[['Nombre', 'IMC', 'Clasificacion IMC']])
    else:
        print("No hay datos registrados.")

# Función para encontrar mayor y menor altura
def altura_extremos():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        mayor_altura = df.loc[df["Estatura (m)"].idxmax()]
        menor_altura = df.loc[df["Estatura (m)"].idxmin()]
        print("\nPersona con mayor altura:")
        print(mayor_altura)
        print("\nPersona con menor altura:")
        print(menor_altura)
    else:
        print("No hay datos registrados.")

# Función para encontrar mayor peso y altura
def peso_altura_max():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        max_peso_altura = df.loc[(df["Peso (kg)"] * df["Estatura (m)"]).idxmax()]
        print("\nPersona con mayor peso y altura:")
        print(max_peso_altura)
    else:
        print("No hay datos registrados.")

# Función para graficar distribución general
def graficar_datos():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        print("\nOpciones de gráficos:")
        print("1. Distribución de IMC")
        print("2. Alturas")
        print("3. Pesos")
        seleccion = input("Elija una opción: ")
        if seleccion == "1":
            df['IMC'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black')
            plt.title("Distribución del IMC")
            plt.xlabel("IMC")
            plt.ylabel("Frecuencia")
            plt.savefig('distribucion_imc.png')
        elif seleccion == "2":
            df['Estatura (m)'].plot(kind='bar', color='lightgreen')
            plt.title("Distribución de Alturas")
            plt.ylabel("Altura (m)")
            plt.savefig('distribucion_alturas.png')
        elif seleccion == "3":
            df['Peso (kg)'].plot(kind='bar', color='lightcoral')
            plt.title("Distribución de Pesos")
            plt.ylabel("Peso (kg)")
            plt.savefig('distribucion_pesos.png')
        else:
            print("Opción no válida.")
            return
        plt.show()
    else:
        print("No hay datos registrados.")

# Función para generar reporte PDF
def generar_reporte_pdf():
    if datos:
        c = canvas.Canvas("reporte_estudiantes.pdf", pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(30, 750, "Reporte de Estudiantes")
        c.drawString(30, 730, "ID    Nombre    Edad    Peso(kg)    Estatura(m)    IMC")
        y = 710
        for estudiante in datos:
            linea = f"{estudiante[0]}    {estudiante[1]}    {estudiante[2]}    {estudiante[3]}    {estudiante[4]}    {estudiante[5]}"
            c.drawString(30, y, linea)
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        print("Reporte PDF generado exitosamente: reporte_estudiantes.pdf")
    else:
        print("No hay datos registrados.")

# Función para categorizar el IMC
def clasificar_imc():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        df['Clasificacion IMC'] = df['IMC'].apply(lambda x: "Peso insuficiente" if x < 18.5 else
                                                 "Peso normal" if x < 24.9 else
                                                 "Sobrepeso" if x < 29.9 else "Obesidad")
        print(df[['Nombre', 'IMC', 'Clasificacion IMC']])
    else:
        print("No hay datos registrados.")

# Función para encontrar mayor y menor altura
def altura_extremos():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        mayor_altura = df.loc[df["Estatura (m)"].idxmax()]
        menor_altura = df.loc[df["Estatura (m)"].idxmin()]
        print("\nPersona con mayor altura:")
        print(mayor_altura)
        print("\nPersona con menor altura:")
        print(menor_altura)
    else:
        print("No hay datos registrados.")

# Función para encontrar mayor peso y altura
def peso_altura_max():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        max_peso_altura = df.loc[(df["Peso (kg)"] * df["Estatura (m)"]).idxmax()]
        print("\nPersona con mayor peso y altura:")
        print(max_peso_altura)
    else:
        print("No hay datos registrados.")

# Función para graficar distribución general
def graficar_datos():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        print("\nOpciones de gráficos:")
        print("1. Distribución de IMC")
        print("2. Alturas")
        print("3. Pesos")
        seleccion = input("Elija una opción: ")
        if seleccion == "1":
            df['IMC'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black')
            plt.title("Distribución del IMC")
            plt.xlabel("IMC")
            plt.ylabel("Frecuencia")
            plt.savefig('distribucion_imc.png')
        elif seleccion == "2":
            df['Estatura (m)'].plot(kind='bar', color='lightgreen')
            plt.title("Distribución de Alturas")
            plt.ylabel("Altura (m)")
            plt.savefig('distribucion_alturas.png')
        elif seleccion == "3":
            df['Peso (kg)'].plot(kind='bar', color='lightcoral')
            plt.title("Distribución de Pesos")
            plt.ylabel("Peso (kg)")
            plt.savefig('distribucion_pesos.png')
        else:
            print("Opción no válida.")
            return
        plt.show()
    else:
        print("No hay datos registrados.")

# Función para generar reporte PDF
def generar_reporte_pdf():
    if datos:
        c = canvas.Canvas("reporte_estudiantes.pdf", pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(30, 750, "Reporte de Estudiantes")
        c.drawString(30, 730, "ID    Nombre    Edad    Peso(kg)    Estatura(m)    IMC")
        y = 710
        for estudiante in datos:
            linea = f"{estudiante[0]}    {estudiante[1]}    {estudiante[2]}    {estudiante[3]}    {estudiante[4]}    {estudiante[5]}"
            c.drawString(30, y, linea)
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        print("Reporte PDF generado exitosamente: reporte_estudiantes.pdf")
    else:
        print("No hay datos registrados.")

# Función para buscar estudiante y mostrar dataframes
def buscar_y_mostrar_estudiantes():
    numero_de_identificacion = entrada_numerica("Ingrese el número de identificación: ", int)
    busqueda(numero_de_identificacion)
    mostrar_datos_dataframe()

# Función para cargar datos desde archivos CSV e imprimirlos
def cargar_y_mostrar_datos():
    cargar_desde_csv()
    mostrar_datos_dataframe()

# Función de búsqueda
def busqueda(numero_de_identificacion):
    for usuario in datos:
        if usuario[0] == numero_de_identificacion:
            print(f"Estudiante encontrado: {usuario}")
            return
    print("Estudiante no registrado.")

# Función para mostrar los datos en un DataFrame
def mostrar_datos_dataframe():
    if datos:
        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        print(df)
    else:
        print("No hay datos registrados.")

# Función principal
def principal():
    cargar_desde_csv()  # Cargar datos al iniciar
    while True:
        print("\n1. Registro de estudiante")
        print("2. Análisis de datos")
        print("3. Graficar datos (IMC, Alturas, Pesos)")
        print("4. Buscar estudiante y mostrar dataframes")
        print("5. Cargar datos desde archivos CSV e imprimirlos")
        print("6. Guardar datos en CSV")
        print("7. Generar reporte PDF")
        print("8. Salir del programa")

        seleccion = input("Escriba su elección: ")

        if seleccion == "1":
            datos_biomedicos()
        elif seleccion == "2":
            submenu_analisis()
        elif seleccion == "3":
            graficar_datos()
        elif seleccion == "4":
            buscar_y_mostrar_estudiantes()
        elif seleccion == "5":
            cargar_y_mostrar_datos()
        elif seleccion == "6":
            guardar_en_csv()
        elif seleccion == "7":
            generar_reporte_pdf()
        elif seleccion == "8":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar programa principal
principal()
