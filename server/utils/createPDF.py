import csv
from fpdf import FPDF
import os
import pandas as pd
from utils.utils import getExperience

def create_pdf(weight=80, genre="Masculino", height=1.70, training_level=1, distance_forearm=30, mass_weight=7.5):
    print("Intento crear el PDF")
    try:
        # Verificar existencia del archivo CSV
        data_file = 'pose_data.csv'
        if not os.path.isfile(data_file):
            print(f"Archivo {data_file} no encontrado.")
            return False

        # Leer el archivo CSV
        df = pd.read_csv(data_file)

        # Crear el objeto PDF
        pdf = FPDF()
        pdf.add_page()

        # Encabezado del PDF
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Reporte de Análisis de Fuerza', 0, 1, 'C')
        pdf.ln(10)

        # Obtener el nivel de entrenamiento
        nivel_entrenamiento = getExperience(training_level)

        # Agregar los datos al PDF
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Datos del análisis', 0, 1, 'C')
        pdf.ln(10)

        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Peso: {weight} kg', 0, 1)
        pdf.cell(0, 10, f'Género: {genre}', 0, 1)
        pdf.cell(0, 10, f'Altura: {height} m', 0, 1)
        pdf.cell(0, 10, f'Nivel de entrenamiento: {nivel_entrenamiento}', 0, 1)
        pdf.cell(0, 10, f'Distancia del antebrazo: {distance_forearm} cm', 0, 1)
        pdf.cell(0, 10, f'Masa de la mancuerna: {mass_weight} kg', 0, 1)
        pdf.ln(10)

        # Obtener la fuerza máxima y promedio
        max_force = df["max_fuerza_bicep"].iloc[0].round(2)
        avg_force = df["average_fuerza_bicep"].iloc[0].round(2)

        # Agregar los datos de fuerza al PDF
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Resultados de Fuerza', 0, 1, 'C')
        pdf.ln(10)

        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Fuerza máxima alcanzada: {max_force} N', 0, 1)
        pdf.cell(0, 10, f'Fuerza promedio: {avg_force} N', 0, 1)
        pdf.ln(10)

        # Agregar las imágenes al PDF
        image_folder = "static"
        if not os.path.isdir(image_folder):
            print(f"Directorio {image_folder} no encontrado.")
            return False

        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Imágenes del análisis', 0, 1, 'C')
        pdf.ln(10)

        for filename in os.listdir(image_folder):
            if filename.endswith('.png'):
                try:
                    pdf.image(os.path.join(image_folder, filename), x=10, y=None, w=190, h=100)
                    pdf.ln(20)  # Ajusta la separación entre imágenes según sea necesario
                except Exception as e:
                    print(f"No se pudo agregar la imagen {filename}: {e}")

        # Pie de página
        pdf.set_y(-15)
        pdf.set_font('Arial', 'I', 8)
        pdf.cell(0, 10, f'Página {pdf.page_no()}', 0, 0, 'C')

        # Guardar el PDF
        output_file = "analisis.pdf"
        pdf.output(output_file)
        print(f"PDF guardado como {output_file}")

        return True
    except Exception as e:
        print(f"Error al crear el PDF: {e}")
        return False
