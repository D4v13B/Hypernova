from datetime import datetime
import json
from graphiti_core import Graphiti
from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient

from models import (
    Agente,
    Cliente,
    ConcretadaCon,
    Interaccion,
    InteraccionesClientes,
    Pago,
    PlanPago,
    PromesaPago,
    ProponePlan,
    RealizaPago,
    RealizadaPor,
    TieneInteraccion,
    Metadata,
)
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, OPEN_API_KEY


class GraphitiClient:
    def __init__(self):
        self.graphiti = None

    @classmethod
    async def create(cls):
        self = cls()
        await self._async_init()
        return self

    async def _async_init(self):
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
        llm_config = LLMConfig(
            api_key="abc",
            model="deepseek-r1:8b",
            small_model="deepseek-r1:8b",
            base_url="http://localhost:11434",
        )

        llm_client = OpenAIClient(config=llm_config)

        self.graphiti = Graphiti(
            uri=NEO4J_URI,
            user=NEO4J_USER,
            password=NEO4J_PASSWORD,
            llm_client=llm_client,
            embedder=OpenAIEmbedder(
                config=OpenAIEmbedderConfig(
                    api_key="abc",
                    embedding_model="nomic-embed-text",
                    embedding_dim=768,
                    base_url="http://localhost:11434/api",
                ),
            ),
            cross_encoder=OpenAIRerankerClient(client=llm_client, config=llm_config),
        )
        await self.graphiti.build_indices_and_constraints()

    async def cargar_datos(self, data: InteraccionesClientes):
        if not self.graphiti:
            raise RuntimeError("Graphiti no está inicializado")

        entity_types = {
            "Cliente": Cliente,
            "Interaccion": Interaccion,
            "Agente": Agente,
            "PlanPago": PlanPago,
            "Pago": Pago,
            "PromesaPago": PromesaPago,
            "Metadata": Metadata,
        }
        edge_types = {
            "TIENE_INTERACCION": TieneInteraccion,
            "REALIZADA_POR": RealizadaPor,
            "PROPONE_PLAN": ProponePlan,
            "REALIZA_PAGO": RealizaPago,
            "CONCRETADA_CON": ConcretadaCon,
        }
        edge_type_map = {
            ("Cliente", "Interaccion"): ["TIENE_INTERACCION"],
            ("Interaccion", "Agente"): ["REALIZADA_POR"],
            ("Interaccion", "PlanPago"): ["PROPONE_PLAN"],
            ("Cliente", "Pago"): ["REALIZA_PAGO"],
            ("PromesaPago", "Pago"): ["CONCRETADA_CON"],
        }

        # 1. Episodio de metadatos
        await self.graphiti.add_episode(
            name="Metadata dataset",
            episode_body=json.dumps(data.metadata.model_dump(), default=str),
            source_description="Información general del lote de datos",
            reference_time=datetime.now(),
            entity_types=entity_types,
            edge_types={},
            edge_type_map={},
        )

        # 2. Episodios por cliente
        for cliente in data.clientes:
            await self.graphiti.add_episode(
                name=f"Cliente {cliente.id}",
                episode_body=json.dumps(cliente.model_dump(), default=str),
                source_description="Carga individual de cliente",
                reference_time=datetime.now(),
                entity_types=entity_types,
                edge_types=edge_types,
                edge_type_map=edge_type_map,
            )

        # 3. Episodios por interacción
        for interaccion in data.interacciones:
            await self.graphiti.add_episode(
                name=f"Interacción {interaccion.id}",
                episode_body=json.dumps(interaccion.model_dump(), default=str),
                source_description="Carga individual de interacción",
                reference_time=datetime.now(),
                entity_types=entity_types,
                edge_types=edge_types,
                edge_type_map=edge_type_map,
            )

        print("Datos cargados en Graphiti ✅ (en lotes pequeños)")
