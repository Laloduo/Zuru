from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import uvicorn
import os
import json

# Configurar FastAPI
app = FastAPI()

# CORS (puedes restringir luego si deseas)
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
    raise ValueError("La clave de OpenAI no está definida.")
client = openai.OpenAI(api_key=openai_api_key)

# Datos de entrada
class ClassificationRequest(BaseModel):
    descripcion: str
    lista: str

# Ejemplo de listas de categorías
LISTAS_CATEGORIAS = {
    "Mercancías Zuru Max": [
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
    "Gases en cilindros",
    "Grasas animales vegetales y minerales en envases de cartón",
    "Grasas animales vegetales y minerales en envases de polietileno",
    "Grasas animales vegetales y minerales en envases metalicos",
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
    "Mercería. Embarques extranjeros",
    "Mercería. Embarques locales",
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
],
    "Mercancías HDI Global": [
    "Abarrotes",
    "Accesorios Computacionales",
    "Aceite automotriz",
    "Aceites y Vinagres",
    "Alfombras, Tapetes y Lámparas",
    "Alimento de Uso Industrial",
    "Artículos de Jardín, Herramientas y Maquinaria",
    "Artículos de Librería",
    "Artículos de Limpieza y Desinfectantes",
    "Artículos para Gimnasio",
    "Ascensores, Escaleras Mecánicas",
    "Automóviles y Camiones",
    "Bebidas Alcohólicas y No Alcohólicas",
    "Boiler",
    "Cables de Cobre y Chatarra Metálica",
    "Café",
    "Calzado en General",
    "Carnes y Productos Congelados",
    "Cemento y Productos Asfálticos",
    "Condimentos y Salsas",
    "Cosméticos y Perfumes",
    "Cueros y Pieles",
    "Dulces en General",
    "Envases de Aluminio y Otros",
    "Equipos Electrónicos",
    "Equipos Médicos e Insumos",
    "Equipos de Audio y Video",
    "Equipos de Comunicación",
    "Equipos de Refrigeración y Aire Acondicionado",
    "Equipos para la Industria Gráfica",
    "Equipos para la Minería",
    "Frutas y Vegetales (Congelados, en Conserva, Frescos, Deshidratados)",
    "Granos Enteros",
    "Herramientas Industriales",
    "Impresos y Publicaciones",
    "Juguetes y Similares",
    "Maquinaria Agrícola",
    "Maquinaria Industrial",
    "Maquinaria Pesada",
    "Materiales Metálicos (Acero, Aluminio, Cobre)",
    "Materiales Plásticos",
    "Materiales de Madera",
    "Materiales para Construcción",
    "Materiales para Techos y Puertas / Ventanas",
    "Mercancías Secas Variadas",
    "Mochilas",
    "Motocicletas y Bicicletas",
    "Muebles, Artículos de Decoración y Construcciones Prefabricadas",
    "Neumáticos y Rodados",
    "Panadería y Pastelería",
    "Papel y Derivados",
    "Perfiles y Planchas de Acero, Aluminio, Madera y Papel",
    "Pescados y Mariscos (Congelados, Frescos, en Conserva)",
    "Pinturas, Recubrimientos y Paneles",
    "Pisos y Revestimientos",
    "Portones, Jaulas y Elementos Estructurales",
    "Productos Farmacéuticos",
    "Productos Lácteos y Derivados",
    "Productos Medicos",
    "Productos de Ferretería",
    "Productos de Higiene y Cuidado Personal",
    "Productos de Iluminación",
    "Productos de Pesca",
    "Repuestos y Accesorios para Maquinaria",
    "Repuestos y Accesorios para Vehículos",
    "Repuestos y Componentes Electrónicos",
    "Ropa y Accesorios de Moda",
    "Snacks (Vegetales Crudos, Yogurt)",
    "Telas, Toallas y Textiles en General",
    "Televisores y Accesorios",
    "Vidrios y Cristales",
],
    "Mercancías Chubb Carga": [
    "Abarrotes en general (exc. vinos y licores) embarques extranjeros",
    "Abarrotes en general (exc. vinos y licores) embarques locales",
    "Aceites minerales, vegetales y animales en carro tanque",
    "Aceites minerales, vegetales y animales en tambores metálicos",
    "Alcohol en lata",
    "Alimentos preparados para animales",
    "Anilinas y colorantes en cunetes de cartón",
    "Anilinas y colorantes en sacos de papel",
    "Anilinas y colorantes líquidos en polvo en envases de plástico rígido",
    "Anilinas y colorantes líquidos en polvo en envases metálicos",
    "Aparatos científicos y médicos",
    "Aparatos de uso doméstico en general",
    "Artículos de escritorio",
    "Artículos de hule",
    "Asbesto-cementos (artículos de)",
    "Barnices en envases metálicos",
    "Barro (curiosidades)",
    "Barro (tubos y análogos)",
    "Bicicletas y motos armadas",
    "Bulbos y cinescopios",
    "Cacao, almendras, y avellanas encostaladas",
    "Cal en envases de papel",
    "Calzado",
    "Carnes congeladas (excluyendo fallas en el sistema de refrigeración)",
    "Casimires",
    "Celofán, papel embobinado",
    "Celulosa en pacas",
    "Cemento en sacos",
    "Cereales y semillas encostaladas",
    "Cerillos y fósforos",
    "Cerveza embotellada",
    "Cerveza y refrescos en lata",
    "Corcho en trozos",
    "Corcho y artículos de (laminados)",
    "Cordelería y costalería",
    "Cristalería",
    "Cuchillería",
    "Cueros y pieles curtidos",
    "Cueros y pieles sin curtir",
    "Discos musicales",
    "Dulces y chocolates (embarques extranjeros)",
    "Dulces y chocolates (embarques locales)",
    "Esponjas naturales",
    "Estructuras metálicas armadas o semi armadas",
    "Ferretería, embarques extranjeros",
    "Ferretería, embarques locales",
    "Fertilizantes en envases de cartón, embarques extranjeros",
    "Fertilizantes en envases de cartón, embarques locales",
    "Fertilizantes en envases de papel, embarques extranjeros",
    "Fertilizantes en envases de papel, embarques locales",
    "Fibras duras preparadas",
    "Focos y tubos fluorescentes",
    "Frutas secas, embarques extranjeros",
    "Frutas, verduras, plantas y flores (no fallas en sist. de refrig.)",
    "Grasas animales vegetales y minerales en envases de cartón",
    "Grasas animales vegetales y minerales en envases de polietileno",
    "Grasas animales vegetales y minerales en envases metálicos",
    "Harina en sacos (Excluido Harina de pescado)",
    "Herramientas ligeras de mano, embarques extranjeros",
    "Herramientas ligeras de mano, embarques locales",
    "Hilos, hilazas, estambres y fibras con envase interior de polietileno",
    "Hilos, hilazas, estambres y fibras sin envase interior de polietileno",
    "Hule crudo, guayule y látex",
    "Insecticidas en polvo en envases de cartón",
    "Insecticidas en polvo en envases de papel",
    "Insecticidas líquidos en envases de plástico rígido",
    "Insecticidas líquidos en tambores metálicos",
    "Instrumentos de precisión",
    "Instrumentos musicales embarques locales",
    "Jabones",
    "Jarciería (instrumentos de limpieza)",
    "Juguetería y artículos deportivos, embarques extranjeros",
    "Juguetería y artículos deportivos, embarques locales",
    "Lanas en pacas",
    "Latería, embarques extranjeros",
    "Latería, embarques locales",
    "Leche en latas",
    "Leche fresca en botellas de plástico o envases de cartón o plástico",
    "Libros y revistas",
    "Linóleums",
    "Madera aserrada",
    "Madera aserrada en trozos",
    "Madera labrada o laminada (triplay)",
    "Máquina de coser, de oficina y de tejer, partes y refacciones",
    "Maquinaria nueva y refacciones",
    "Maquinaria, equipo de contratista",
    "Mariscos y pescados (no daños por falla en el sistema de refrigeración)",
    "Mármoles y pizarras en bloques",
    "Mármoles y pizarras en planchas",
    "Materiales eléctricos (excepto frágiles)",
    "Medicinas de patente",
    "Melazas en carros tanque pipa o cisternas",
    "Menaje de casa",
    "Mercería, embarques extranjeros",
    "Mercería, embarques locales",
    "Metales no preciosos en barras o telas (excluye cobre)",
    "Metales no preciosos en laminados (excluye cobre)",
    "Miel en tambores metálicos",
    "Minerales no preciosos en bruto",
    "Minerales precipitados y concentrados no preciosos",
    "Mosaicos y azulejos",
    "Motores, bombas, bobinas y transformadores eléctricos",
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
    "Pianos, órganos y análogos, embarques extranjeros",
    "Pianos, órganos y análogos, embarques locales",
    "Piel y cuero, artículos de",
    "Pinturas en latas metálicas",
    "Plásticos, artículos de",
    "Polietileno y similares para elaboración de fibras textiles, en cunetes",
    "Polietileno y similares para elaboración de fibras textiles, en envases",
    "Productos químicos en damajuanas",
    "Productos químicos en polvo en envases de cartón",
    "Productos químicos en polvo en envases de papel o de polietileno",
    "Productos químicos inflamables en envases de plástico rígido",
    "Productos químicos no inflamables en envases de plástico rígido",
    "Productos químicos no inflamables en tambores metálicos",
    "Refacciones para autos y motos, excluyendo artículos frágiles, embarques extranjeros",
    "Refrescos embotellados",
    "Ropa hecha, botonería y lencería, embarques extranjeros",
    "Ropa hecha, botonería y lencería, embarques locales",
    "Sal envasada",
    "Tapetes y alfombras",
    "Telas en fardos, embarques extranjeros",
    "Telas en fardos, embarques locales",
    "Tubería metálica",
    "Varilla de acero",
    "Vidrio plano",
    "Vidrio, artículos de",
    "Viguetas de acero",
    "Vinos y licores embotellados, embarques extranjeros",
    "Vinos y licores embotellados, embarques locales",
    "Vinos y licores en pipa o carro tanque",
    "Yeso en sacos",
]
}

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
    return {"mensaje": "Clasificador multi-lista activo 🎯"}

@app.post("/classify")
async def classify(request: ClassificationRequest):
    descripcion = request.descripcion.strip().lower()
    nombre_lista = request.lista.strip()

    if nombre_lista not in LISTAS_CATEGORIAS:
        raise HTTPException(status_code=400, detail="Lista de categorías inválida.")

    categorias = LISTAS_CATEGORIAS[nombre_lista]
    clave_memoria = f"{descripcion}__{nombre_lista}"
    memoria = cargar_memoria()

    if clave_memoria in memoria:
        return {"categoria": memoria[clave_memoria]}

    prompt = f"""
Eres un asistente de inteligencia artificial experto en clasificación de mercancías para seguros y logística.

Tu función es clasificar mercancías en **UNA SOLA** de las siguientes categorías:
{', '.join(categorias)}

📌 Instrucciones clave:
1. Si la descripción contiene una palabra o frase que coincida total o parcialmente con una categoría, selecciona esa categoría obligatoriamente.
2. Si no hay coincidencia directa, elige la categoría que más se aproxime en función del **uso, naturaleza o función del producto**.
3. La comparación debe ser robusta: detecta coincidencias aún si hay errores menores de escritura o diferencias de idioma (español, inglés o alemán).
4. Solo si **ninguna categoría es razonablemente aplicable**, responde exactamente: **Sin clasificar**.
5. Nunca respondas con explicaciones, sinónimos ni sugerencias.
6. Responde **solo** con el nombre exacto de la categoría (copiado literalmente) o con **"Sin clasificar"**.

Ejemplos:
- Si la descripción es "yeso", responde: **Yeso en sacos**
- Si la descripción es "corcho", responde: **Corcho en trozos**
- "producto inexistente zzz123" → **Sin clasificar**

📦 Descripción del producto:
\"\"\"{request.descripcion}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        categoria = response.choices[0].message.content.strip()
        memoria[clave_memoria] = categoria
        guardar_memoria(memoria)
        return {"categoria": categoria}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
