import asyncio
import logging
from data_proceso_lectura import cargar_validar_json
from pathlib import Path
from GraphitiClient import GraphitiClient

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "interacciones_clientes2.json"

async def main():

    # Cargar y validar JSON
    data = cargar_validar_json(DATA_FILE)

    #Init Graphiti
    client = GraphitiClient()
    await client._async_init()
    # Cargar datos en Graphiti
    await client.cargar_datos(data)
    # print(data)
    # print(DATA_FILE)

    print("Pipeline completado ✅")


if __name__ == "__main__":
    asyncio.run(main())
