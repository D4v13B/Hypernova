import json
import logging
from datetime import datetime
from pydantic import ValidationError
from typing import List, Dict, Any
import asyncio
from graphiti_core.driver.neo4j_driver import Neo4jDriver

# Asume que estos modelos están definidos en `models.py`
from models import (
    Agente,
    Cliente,
    Interaccion,
    InteraccionesClientes,
    Pago,
    PlanPago,
    PromesaPago,
    Metadata
)
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, OPEN_API_KEY
from graphiti_core import Graphiti
from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient

logger = logging.getLogger(__name__)

class GraphitiClient:
    def __init__(self):
        self.graphiti = None
        self.schema_configured = False

    @classmethod
    async def create(cls):
        """Async factory method to create and initialize the Graphiti client."""
        self = cls()
        await self._async_init()
        return self

    async def _async_init(self):
        """Initializes the Graphiti client with LLM and embedding configurations."""
        try:
            # self.graphiti = Graphiti(
            #     uri=NEO4J_URI,
            #     user=NEO4J_USER,
            #     password=NEO4J_PASSWORD,
            #     llm_client=GeminiClient(
            #         config=LLMConfig(api_key=OPEN_API_KEY, model="gemini-2.0-flash")
            #     ),
            #     embedder=GeminiEmbedder(
            #         config=GeminiEmbedderConfig(
            #             api_key=OPEN_API_KEY, embedding_model="embedding-001"
            #         )
            #     ),
            #     cross_encoder=GeminiRerankerClient(
            #         config=LLMConfig(api_key=OPEN_API_KEY, model="gemini-2.0-flash-exp")
            #     ),
            # )
            self.graphiti = Graphiti(
                graph_driver=Neo4jDriver(
                    uri=NEO4J_URI,
                    password=NEO4J_PASSWORD,
                    user=NEO4J_PASSWORD,
                    database='neo4j'
                )
            )
            await self.graphiti.build_indices_and_constraints()
            self.schema_configured = True
            logger.info("✅ Cliente de Graphiti inicializado y esquema construido.")
        except Exception as e:
            logger.error(f"❌ Error durante la inicialización del cliente de Graphiti: {e}")
            raise

    async def cargar_datos(self, data: InteraccionesClientes, batch_size: int = 50):
        """
        Carga los datos en Graphiti por lotes, usando el método add_episode.
        """
        if not self.schema_configured:
            raise RuntimeError("El cliente de Graphiti no está inicializado. Llama a .create() primero.")

        episodes_to_ingest = []

        # Convertir clientes a episodios
        for cliente in data.clientes:
            episodes_to_ingest.append({
                "name": f"Cliente {cliente.id}",
                "episode_body": json.dumps(cliente.model_dump(mode='json')),
                "source_description": "Datos de cliente",
                "reference_time": cliente.fecha_prestamo,
            })
        
        # Convertir interacciones a episodios
        for interaccion in data.interacciones:
            episodes_to_ingest.append({
                "name": f"Interacción {interaccion.id}",
                "episode_body": json.dumps(interaccion.model_dump(mode='json')),
                "source_description": "Datos de interacción",
                "reference_time": interaccion.timestamp,
            })
        
        total_episodes = len(episodes_to_ingest)
        logger.info(f"📦 Preparando {total_episodes} episodios para la ingestión.")
        
        # Procesar los episodios en lotes
        for i in range(0, total_episodes, batch_size):
            batch = episodes_to_ingest[i:i + batch_size]
            try:
                tasks = [self.graphiti.add_episode(**episode) for episode in batch]
                await asyncio.gather(*tasks)
                logger.info(f"🎉 Lote {int(i/batch_size) + 1} de {len(batch)} episodios cargado exitosamente.")
            except Exception as e:
                logger.error(f"❌ Error al cargar el lote de episodios: {e}")
                raise

        logger.info("✅ Carga de todos los datos completada.")