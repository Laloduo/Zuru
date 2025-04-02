import os
from dotenv import load_dotenv
import openai

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API desde las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Verificar si la API Key está cargada correctamente
if not api_key:
    print("❌ ERROR: No se encontró la API Key en .env")
else:
    print("✅ API Key cargada correctamente")

# Probar si OpenAI responde
try:
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Hola, responde con un saludo."}]
    )
    print("✅ OpenAI responde:", response["choices"][0]["message"]["content"])
except Exception as e:
    print("❌ ERROR en la conexión con OpenAI:", e)
