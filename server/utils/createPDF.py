import csv
from fpdf import FPDF
import os

def create_pdf(weight=80, genre="Masculino", height=1.70, training_level=1, distance_forearm=30, mass_weight=7.5):
    print("Intento crear el PDF")
    try:
        # Verificar existencia del archivo CSV
        data_file = 'pose_data.csv'
        if not os.path.isfile(data_file):
            print(f"Archivo {data_file} no encontrado.")
            return False

        # Leer el archivo CSV
        data = []
        with open(data_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        # Crear el objeto PDF
        pdf = FPDF()
        pdf.add_page()
        print("Creo el PDF")

        # Agregar los datos al PDF
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Datos del análisis', ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Peso: {weight}', ln=True)
        pdf.cell(0, 10, f'Género: {genre}', ln=True)
        pdf.cell(0, 10, f'Altura: {height}', ln=True)
        pdf.cell(0, 10, f'Nivel de entrenamiento: {training_level}', ln=True)
        pdf.cell(0, 10, f'Distancia del antebrazo: {distance_forearm}', ln=True)
        pdf.cell(0, 10, f'Masa del peso: {mass_weight}', ln=True)
        pdf.ln(10)

        print("Agrego los datos al PDF")
        # Obtener la fuerza máxima y promedio
        max_force = 13
        avg_force = 12
        print("Agrego max_force y avg_force al PDF")
        # Agregar los datos de fuerza al PDF
        pdf.cell(0, 10, f'Fuerza máxima alcanzada: {max_force}', ln=True)
        pdf.cell(0, 10, f'Fuerza promedio: {avg_force}', ln=True)
        pdf.ln(10)

        # Agregar las imágenes al PDF
        image_folder = "static"
        if not os.path.isdir(image_folder):
            print(f"Directorio {image_folder} no encontrado.")
            return False

        for filename in os.listdir(image_folder):
            if filename.endswith('.png'):
                try:
                    pdf.image(os.path.join(image_folder, filename), x=10, y=None, w=0, h=100)
                except Exception as e:
                    print(f"No se pudo agregar la imagen {filename}: {e}")

        # Guardar el PDF
        output_file = "analisis.pdf"
        pdf.output(output_file)
        print(f"PDF guardado como {output_file}")

        return True
    except Exception as e:
        print(f"Error al crear el PDF: {e}")
        return False

