import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


st.set_page_config(page_title="Formulario académico", layout="centered")
st.title("Formulario académico: Impacto de la IA en el mercado laboral post-pandemia")
st.markdown("Este formulario es parte de un trabajo universitario. Tus respuestas son anónimas y serán utilizadas solo con fines académicos.")

# Sección 1: Datos generales
st.header("Sección 1: Datos Generales")
edad = st.selectbox("¿Cuál es su edad?", ["18–25", "26–35", "36–45", "Más de 45"])

# Sección 2: Implementación de la Inteligencia Artificial
st.header("Sección 2: Implementación de la Inteligencia Artificial")
st.markdown("**Del 1 al 5, donde 1 = Totalmente en desacuerdo y 5 = Totalmente de acuerdo.**")

ia_preguntas = [
    "En mi lugar de trabajo se han automatizado muchas tareas rutinarias.",
    "Algunas funciones han sido reemplazadas por herramientas digitales.",
    "Se utilizan tecnologías con inteligencia artificial en procesos laborales.",
    "Existen sistemas con IA integrados en las actividades diarias.",
    "La IA ha mejorado la eficiencia en las operaciones de mi empresa.",
    "El personal ha recibido capacitación para el uso de herramientas con IA.",
    "Se interactúa regularmente con herramientas automatizadas.",
    "Hay interés institucional por ampliar el uso de inteligencia artificial.",
    "La adopción de IA ha sido gradual y organizada.",
    "La IA ha transformado procesos clave dentro de mi organización."
]
ia_respuestas = []
for i, p in enumerate(ia_preguntas):
    st.markdown(f"**Pregunta {i+1}**")
    ia_respuestas.append(st.slider(p, 1, 5, 3, key=f"ia_{i+1}"))

# Sección 3: Transformación del Mercado Laboral
st.header("Sección 3: Transformación del Mercado Laboral")
st.markdown("**Del 1 al 5, donde 1 = Totalmente en desacuerdo y 5 = Totalmente de acuerdo.**")

laboral_preguntas = [
    "La automatización ha ocasionado pérdida de empleos en mi sector.",
    "Han surgido nuevos roles laborales relacionados con inteligencia artificial.",
    "Se exigen nuevas competencias digitales para los mismos puestos.",
    "He debido aprender nuevas herramientas digitales por exigencias del trabajo.",
    "La IA podría afectar mi puesto si no me actualizo constantemente.",
    "Mi organización promueve la formación continua frente a la transformación digital.",
    "Se ofrecen talleres o capacitaciones sobre IA.",
    "El personal muestra disposición para adaptarse a nuevas tecnologías.",
    "Conozco casos cercanos de desplazamiento laboral debido a IA.",
    "Considero la IA más una oportunidad que una amenaza.",
    "Las habilidades digitales son valoradas en mi entorno laboral.",
    "Se prioriza contratar perfiles con formación tecnológica.",
    "Se combinan habilidades blandas y técnicas en los nuevos puestos.",
    "La estructura tradicional del trabajo se ha visto modificada.",
    "Mi organización tiene políticas claras para integrar nuevas tecnologías."
]
laboral_respuestas = []
for i, p in enumerate(laboral_preguntas):
    st.markdown(f"**Pregunta {i+11}**")
    laboral_respuestas.append(st.slider(p, 1, 5, 3, key=f"lab_{i+11}"))

# Envío del formulario
if st.button("Enviar formulario"):
    # 1. Autenticación con Google Sheets usando credenciales desde secrets.toml
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    service_account_info = {
        "type": st.secrets["google_service_account"]["type"],
        "project_id": st.secrets["google_service_account"]["project_id"],
        "private_key_id": st.secrets["google_service_account"]["private_key_id"],
        "private_key": st.secrets["google_service_account"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["google_service_account"]["client_email"],
        "client_id": st.secrets["google_service_account"]["client_id"],
        "auth_uri": st.secrets["google_service_account"]["auth_uri"],
        "token_uri": st.secrets["google_service_account"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google_service_account"]["client_x509_cert_url"]
    }

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(credentials)


    nombre_hoja = "Respuestas_Formulario_IA"
    sheet = client.open(nombre_hoja).sheet1

    # 3. Preparar encabezados y datos
    encabezados = ["Edad"] + [f"IA Pregunta {i+1}" for i in range(len(ia_preguntas))] + [f"Laboral Pregunta {i+1}" for i in range(len(laboral_preguntas))]
    fila = [edad] + ia_respuestas + laboral_respuestas

 
    # 4. Si la hoja no tiene encabezados, los agregamos
    primer_fila = sheet.row_values(1)
if not primer_fila or all(cell.strip() == "" for cell in primer_fila):
    sheet.insert_row(encabezados, 1)

    # 5. Enviar datos
    sheet.append_row(fila)

    st.success("¡Gracias por tu participación! Tus respuestas han sido registradas en Google Sheets.")
