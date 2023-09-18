import pandas as pd
import folium
import re
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

# Función para extraer coordenadas
def extract_coordinates(geom):
    match = re.search(r'POINT \(([^)]+)\)', geom)
    if match:
        coordinates = match.group(1).split()
        if len(coordinates) == 2:
            return float(coordinates[1]), float(coordinates[0])  # Cambia el orden a (latitud, longitud)
    return None

df = pd.read_csv('datasets.csv')

df = df.drop('ADDRESS2', axis=1)

df_limpio = df.drop_duplicates()

mask = df_limpio['CITY'] == 'Brooklyn'
df_limpio = df_limpio[mask]

df_limpio = df_limpio.nlargest(3, 'GRADING')

# Crear un mapa con Folium
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)  # Nueva York como ubicación inicial

# Marcar las ubicaciones de los tres mejores lugares en el mapa
for index, row in df_limpio.iterrows():
    name = row['NAME']
    coordinates = extract_coordinates(row['the_geom'])
    if coordinates:
        lat, lon = coordinates
        popup_text = f"{name}, GRADING: {row['GRADING']}"
        folium.Marker([lat, lon], popup=popup_text).add_to(m)

m.save('mapa_top_3_lugares.html')

# Tomar una captura de pantalla del mapa HTML
img_data = m._to_png()
img = PILImage.open(io.BytesIO(img_data))
img.save('mapa_screenshot.png')

# Crear un informe en PDF
pdf_file = 'informe.pdf'

c = canvas.Canvas(pdf_file, pagesize=letter)
c.setFont('Helvetica', 14)

# Título
c.drawString(100, 750, 'Informe de los 3 mejores lugares en Brooklyn')
c.line(100, 740, 500, 740)
c.setFont('Helvetica', 12)
# Agregar la captura de pantalla del mapa
map_screenshot = 'mapa_screenshot.png'
c.drawImage(map_screenshot, 100, 420, width=400, height=300)
print(df_limpio['NAME'])
# Agregar lista de los 3 mejores lugares
c.drawString(100, 400, 'Los 3 mejores lugares en Brooklyn:')
for i, row in enumerate(df_limpio.itertuples(), start=1):
    place_name = row.NAME
    place_grading = row.GRADING
    c.drawString(120, 380 - (i - 1) * 20, f"{i}. {place_name} - GRADING: {place_grading}")

github_url = 'https://github.com/AH1819/Big-data/tree/main/tareas/practica-3/'
c.drawString(100, 50, f'URL de GitHub: {github_url}')

c.save()

print(f"Informe generado y guardado como '{pdf_file}'")
