from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import uvicorn
import os
import json

# Configurar FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key desde entorno
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("La clave de OpenAI no está definida en las variables de entorno.")
client = openai.OpenAI(api_key=openai_api_key)

# Categorías disponibles (igual que en tu código actual)
CATEGORIES = [
    "Abarrotes en general (exc. vinos y licores) embarques extranjeros",
    "Abarrotes en general (exc. vinos y licores) embarques locales",
    "Abatelenguas y guantes de latex",
    "Aceites minerales, vegetales y animales en carro tanque",
    "Aceites minerales, vegetales y animales en tambores metálicos",
    "Alcohol en lata",
    "Algodón y borras en pacas",
    "Alimentos preparados para animales",
    "Anilinas y colorantes en cunetes de cartón",
    "Anilinas y colorantes en sacos de papel",
    "Anilinas y colorantes líquidos en polvo en envases de plástico rígido",
    "Anilinas y colorantes líquidos en polvo en envases metálicos",
    "Aparatos científicos y medicos",
    "Aparatos de uso doméstico en general",
    "Artículos de cocina",
    "Artículos de cuidado e higiene para bebés",
    "Artículos de dormitorio (Ropa de cama)",
    "Artículos de escritorio",
    "Asbesto-cementos (articulos de)",
    "Autopartes",
    "Azúcar encostalada",
    "Barnices en envases metalicos",
    "Barro (curiosidades)",
    "Barro (tubos y analogos)",
    "Bicicletas y motos armadas",
    "Bulbos y cinescopios",
    "Cacao, almendras, y avellanas encostaladas",
    "Cafe encostalado",
    "Cal en envases de papel",
    "Calzado",
    "Camaras y articulos fotograficos (excluyendo películas)",
    "Carnes congeladas (excluyendo fallas en el sistema de refrigeración)",
    "Carnes congeladas (incluyendo fallas en el sistema de refrigeración)",
    "Casimires",
    "Celofan, papel embobinado",
    "Celulosa en pacas",
    "Cemento en sacos",
    "Cereales y semillas encostaladas",
    "Cerillos y fósforos",
    "Cerveza embotellada",
    "Cerveza y refrescos en lata",
    "Copra",
    "Corcho en trozos",
    "Corcho y artículos de (laminados)",
    "Cordelería y costalería",
    "Cristalería",
    "Cuchillería",
    "Cueros y Pieles",
    "Cueros y pieles curtidos",
    "Cueros y pieles sin curtir",
    "Discos musicales",
    "Dulces y chocolates (embarques extranjeros)",
    "Dulces y chocolates (embarques locales)",
    "Electrodomésticos linea blanca",
    "Equipo Electrónico, refacciones y similares (Excluye Celulares, Tablets, Drones, Scooter)",
    "Equipos tecnológicos (incluye celulares, tablets, drones, scooter)",
    "Esponjas naturales",
    "Estructuras metalicas armadas o semi armadas",
    "Ferretería, Embarques extranjeros",
    "Ferretería, Embarques locales",
    "Fertilizantes en envases de cartón, Embarques extranjeros",
    "Fertilizantes en envases de cartón, Embarques locales",
    "Fertilizantes en envases de papel, Embarques extranjeros",
    "Fertilizantes en envases de papel, Embarques locales",
    "Fibras duras preparadas",
    "Focos y tubos fluorecentes",
    "Frutas secas. Embarques extranjeros.",
    "Frutas secas. Embarques locales",
    "Frutas, verduras, plantas y flores. (incluyendo fallas en el sistema de refrigeración)",
    "Frutas, verduras, plantas y flores. (no fallas en sist. de refrig.)",
    "Ganado y aves de pie",
    "Gases en cilindros",
    "Grasas animales vegetales y minerales en envases de cartón",
    "Grasas animales vegetales y minerales en envases de polietileno",
    "Grasas animales vegetales y minerales en envases metalicos",
    "Harina de pescado",
    "Harina en sacos",
    "Herramientas ligeras de mano. Embarques extranjeros",
    "Herramientas ligeras de mano. Embarques locales",
    "Hilos, hilazas, estambres y fibras con envase interior de polietileno dentro de cajas de cartón",
    "Hilos, hilazas, estambres y fibras sin envase interior de polietileno",
    "Huevo",
    "Hule crudo, guayale y latex",
    "Insecticidas en polvo, en envases de cartón",
    "Insecticidas en polvo, en envases de papel",
    "Insecticidas líquidos en envases de plastico rigido",
    "Insecticidas líquidos en tambos metalicos",
    "Instrumentos de precisión",
    "Instrumentos musicales Embarques extranjeros",
    "Instrumentos musicales Embarques locales",
    "Jabones",
    "Jarciería (Instrumentos de Limpieza)",
    "Joyería de fantasía y artesanías metalicas",
    "Juguetería y artículos deportivos. Embarques extranjeros",
    "Juguetería y artículos deportivos. Embarques locales",
    "Lanas en pacas",
    "Latería. Embarques extranjeros",
    "Latería. Embarques locales",
    "Leche en latas",
    "Leche en pipas",
    "Leche fresca en botellas de plastico o envases de cartón o plastico",
    "Leche fresca en botes metalicos",
    "Libros y revistas",
    "Linoleums",
    "Llantas y artefactos de hule",
    "Madera aserrada",
    "Madera aserrada en trozozs",
    "Madera labrada o laminada (triplay)",
    "Maquina de coser, de oficiona y de tejer, partes y refacciones",
    "Maquinaria nueva y refacciones",
    "Maquinaria, Equipo de contratista",
    "Mariscos y pescados, (no danos por falla en el sistema de refrigeración)",
    "Mariscos y pescados,(incluyendo fallas en el sistema de refrigeración)",
    "Marmoles y pizarras en bloques",
    "Marmoles y pizarras en planchas",
    "Materiales electricos (excepto fragiles)",
    "Medicinas de patente",
    "Melazas en carros, tanque pipa o cisternas",
    "Menaje de casa",
    "Mercería. Embarques extranjeros",
    "Mercería. Embarques locales",
    "Metales no preciosos (incluye cobre)",
    "Metales no preciosos en barras o telas (excluye cobre)",
    "Metales no preciosos en laminados (excluye cobre)",
    "Miel en tambores metalicos",
    "Minerales no preciosos en bruto",
    "Minerales precipitados y concentrados no preciosos",
    "Moldes de plástico automotrices",
    "Mosaicos y azulejos",
    "Motores, bombas, bobinas y transformadores electricos",
    "Muebles nuevos de madera",
    "Muebles nuevos de metal",
    "Muebles sanitarios",
    "Papel embobinado",
    "Papelería",
    "Paraguas y sombrillas",
    "Película virgen en rollos para procesamiento",
    "Película virgen en rollos terminados",
    "Películas filmadas",
    "Perfiles de aluminio",
    "Perfumería",
    "Petróleo y sus derivados en tanques",
    "Pianos, órganos y analogos. Embarques extranjeros",
    "Pianos, órganos y analogos. Embarques locales",
    "Piel y cuero, artículos de",
    "Pinturas en latas metalicas",
    "Plasticos, artículos de",
    "Polietileno y similares para elaboración de fibras textiles, en cunetes",
    "Polietileno y similares para elaboración de fibras textiles, en envases de cartón",
    "Polietileno y similares para elaboración de fibras textiles, en envases de polietileno",
    "Productos químicos en damajuanas",
    "Productos químicos en polvo en envases de cartón",
    "Productos químicos en polvo en envases de papel o de polietileno",
    "Productos químicos inflamables en envases de plastico rígido",
    "Productos químicos no inflamables en envases de plastico rígido",
    "Productos químicos no inflamables en tambores metalicos",
    "Refacciones para autos y motos, exc. art. frágiles. Embarques extranj",
    "Refacciones para autos y motos, exc. art. frágiles. Embarques locales",
    "Refrescos embotellados",
    "Relojería",
    "Repuestos electrónicos",
    "Repuestos plásticos",
    "Ropa hecha, botonería y lencería. Embarques extranjeros",
    "Ropa hecha, botonería y lencería. Embarques locales",
    "Ropa y Artículos de seguridad",
    "Sal envasada",
    "Tapetes y alfombras",
    "Telas fardos. Embarques extranjeros",
    "Telas fardos. Embarques locales",
    "Tubería metálica",
    "Varilla de acero",
    "Vidrio plano",
    "Vidrio, artículos de",
    "Viguetas de acero",
    "Vinos y licores embotellados. Embarques extranjeros",
    "Vinos y licores embotellados. Embarques locales",
    "Vinos y licores en pipa o carro tanque",
    "Yeso en sacos",
]  # ← Aquí pegas tus categorías completas (por tamaño no las copio todas aquí)

# Modelo de datos
class ClassificationRequest(BaseModel):
    descripcion: str

# Archivo de memoria
MEMORIA_PATH = "memoria.json"

def cargar_memoria():
    if not os.path.exists(MEMORIA_PATH):
        return {}
    with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_memoria(memoria):
    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

@app.get("/")
def home():
    return {"mensaje": "¡Clasificación con GPT-4 funcionando con memoria!"}

@app.post("/classify")
async def classify(request: ClassificationRequest):
    descripcion = request.descripcion.strip().lower()
    memoria = cargar_memoria()

    # Si ya fue clasificado antes
    if descripcion in memoria:
        return {"categoria": memoria[descripcion]}

    # Generar prompt
    prompt = f"""
    Eres un asistente de inteligencia artificial experto en clasificación de productos.

    Analiza la siguiente descripción (puede contener errores ortográficos o lenguaje informal) y clasifícala en **una sola** de las siguientes categorías: {', '.join(CATEGORIES)}.

    Si la descripción es ambigua pero parece estar relacionada con un producto, selecciona la categoría más adecuada posible.
    Si la descripción **no tiene ninguna relación con un producto**, responde con **"Sin coincidencias claras"**.
    Si no puedes asignarla razonablemente a ninguna categoría, responde con **"Otros"**.

    Descripción del producto:
    "{request.descripcion}"

    Responde únicamente con una de las siguientes opciones:
    - El nombre exacto de la categoría correspondiente
    - "Otros"
    - "Sin coincidencias claras"

    No agregues explicaciones ni texto adicional.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        categoria_predicha = response.choices[0].message.content.strip()

        # Verifica si es válida o una excepción permitida
        if categoria_predicha not in CATEGORIES and categoria_predicha not in ["Otros", "Sin coincidencias claras"]:
            raise HTTPException(status_code=400, detail="La respuesta no es una categoría válida")

        # Guardar en memoria
        memoria[descripcion] = categoria_predicha
        guardar_memoria(memoria)

        return {"categoria": categoria_predicha}

    except openai.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"Error de OpenAI: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
