import json
import logging
from models import InteraccionesClientes

logger = logging.getLogger(__name__)


def cargar_validar_json(path: str) -> InteraccionesClientes:
    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    try:
        data = InteraccionesClientes(**raw_data)
        logger.info(
            f"Validación exitosa: {len(data.clientes)} clientes, {len(data.interacciones)} interacciones"
        )
        return data
    except Exception as e:
        logger.error(f"Error de validación: {e}")
        raise
