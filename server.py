from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import uvicorn

# Configurar FastAPI
app = FastAPI()

# Configurar CORS para permitir conexiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar la API Key desde una variable de entorno
import os
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("La clave de OpenAI no está definida en las variables de entorno.")

client = openai.OpenAI(api_key=openai_api_key)

# Definir las categorías disponibles
CATEGORIES = [
    "Automóviles y Camiones", "Ascensores", "Boiler", "Juguetes", "Productos de Pesca", 
    "Pescados y Mariscos", "Calzado en General", "Cosméticos y Perfumes", "Accesorios Computacionales"
]

# Modelo de datos de entrada
class ClassificationRequest(BaseModel):
    descripcion: str

@app.get("/")
def home():
    return {"mensaje": "¡Clasificación con GPT-4 funcionando!"}

@app.post("/classify")
async def classify(request: ClassificationRequest):
    prompt = f"""
    Eres un asistente de inteligencia artificial experto en clasificar productos.
    Categoriza la siguiente descripción en una de estas categorías: {', '.join(CATEGORIES)}.
    
    Descripción: "{request.descripcion}"
    
    Solo responde con la categoría exacta, sin explicaciones adicionales.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        categoria_predicha = response.choices[0].message.content.strip()
        
        if categoria_predicha not in CATEGORIES:
            raise HTTPException(status_code=400, detail="La respuesta no es una categoría válida")
        
        return {"categoria": categoria_predicha}
    
    except openai.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"Error de OpenAI: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

