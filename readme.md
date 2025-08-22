# Hypernova: Exploración de Grafos de Conocimiento para Interacciones con Clientes

## Descripción de la Solución

Hypernova es una prueba técnica que explora la construcción de un grafo de conocimiento para analizar las interacciones con clientes. El objetivo era comprender la viabilidad de utilizar grafos para modelar y analizar las relaciones entre clientes, interacciones (llamadas, emails, SMS, pagos), agentes, planes de pago y promesas de pago.

A pesar de los desafíos encontrados (detallados más adelante), el proyecto logró establecer las bases para un sistema que podría, en el futuro, proporcionar una visión holística de las relaciones con los clientes, permitiendo:

*   **Modelado de Datos:** Definición de modelos de datos robustos utilizando Pydantic para representar las entidades y relaciones clave en el dominio de las interacciones con clientes.
*   **Comprensión del Concepto:** Profundo entendimiento de los principios de los grafos de conocimiento y su aplicación al análisis de interacciones con clientes.
*   **Establecimiento de Relaciones:** Definición y modelado de las relaciones entre las diferentes entidades, creando un grafo interconectado que refleja la complejidad de las interacciones con clientes.

## Instrucciones de Instalación Paso a Paso

1.  **Requisitos Previos:**

    *   Asegúrate de tener instalados Docker y Docker Compose en tu sistema.  Puedes descargarlos desde [Docker Desktop](https://www.docker.com/products/docker-desktop/).
    *   Python 3.10 o superior.

2.  **Clonar el Repositorio:**

    ```bash
    git clone https://github.com/D4v13B/Hypernova
    cd Hypernova/backend
    ```

3.  **Configurar las Variables de Entorno:**

    *   Crea un archivo `.env` en el directorio `backend`.
    *   Agrega las siguientes variables de entorno al archivo `.env`:

        ```
        NEO4J_URI=bolt://localhost:7687
        NEO4J_USER=neo4j
        NEO4J_PASSWORD=password123
        GEMINI_API_KEY=<TU_CLAVE_DE_API_DE_GEMINI>
        ```

        **Nota:** Reemplaza `<TU_CLAVE_DE_API_DE_OPENAI>` con tu clave de API de OpenAI si planeas utilizar las capacidades de procesamiento de lenguaje natural de Graphiti. Si no planeas usar estas características, puedes dejar esta variable vacía.  La contraseña por defecto de Neo4j es `password123`.

4.  **Ejecutar con Docker Compose:**

    ```bash
    docker-compose up -d
    ```

    Este comando descargará las imágenes necesarias, creará los contenedores para Neo4j y Graphiti, y los ejecutará en segundo plano.

5.  **Instalar las Dependencias de Python:**

    ```bash
    pip install -r requirements.txt
    ```

    Este comando instalará todas las bibliotecas de Python necesarias para ejecutar el backend.

## Cómo Ejecutar el Proyecto

1.  **Cargar los Datos:**

    Una vez que los contenedores de Docker estén en funcionamiento y las dependencias de Python estén instaladas, puedes cargar los datos de interacción con los clientes en el grafo de conocimiento.  Ejecuta el script `main.py`:

    ```bash
    python main.py
    ```

    Este script leerá los datos del archivo `interacciones_clientes2.json` (ubicado en el directorio `data`) y los cargará en la base de datos Neo4j a través de Graphiti.

## Decisiones Técnicas Importantes

*   **Elección de `graphiti-core`:** Inicialmente, se seleccionó `graphiti-core` para simplificar la interacción con Neo4j y explorar sus capacidades de LLM y embeddings. Sin embargo, durante el desarrollo, surgieron problemas de compatibilidad y errores de sintaxis en las consultas Cypher generadas por la librería, lo que llevó a considerar alternativas.
*   **Consideración de Zep:** Debido a los problemas encontrados con `graphiti-core`, se evaluó la posibilidad de migrar a Zep, otra librería para la construcción de grafos de conocimiento. Sin embargo, debido a las limitaciones de tiempo y al alcance de la prueba técnica, se decidió continuar con `graphiti-core` para completar los objetivos iniciales.
*   **Pydantic para la Definición de Modelos:** Se utilizó Pydantic para definir los modelos de datos (Cliente, Interaccion, etc.) debido a su capacidad para validar los datos y generar documentación automáticamente.

## Desafíos Encontrados

*   **Problemas con `graphiti-core`:** Se encontraron dificultades para configurar y utilizar `graphiti-core` debido a errores de sintaxis en las consultas Cypher generadas por la librería. Esto requirió una investigación exhaustiva y la implementación de soluciones alternativas.

## Mejoras Futuras Identificadas

*   **Evaluación Exhaustiva de Alternativas:** Realizar una evaluación exhaustiva de diferentes librerías para la construcción de grafos de conocimiento, incluyendo Zep, para determinar la mejor opción para las necesidades del proyecto.
*   **Integración con Herramientas de Análisis de Datos:**  Integrar Hypernova con herramientas de análisis de datos como Pandas, Scikit-learn o Spark para realizar análisis más avanzados y construir modelos de machine learning.
*   **Implementación de un Sistema de Recomendación:**  Desarrollar un sistema de recomendación que sugiera estrategias de contacto y planes de pago personalizados para cada cliente, basándose en su historial de interacciones y su perfil.
*   **Mejora del Manejo de Errores:**  Implementar un manejo de errores más robusto y detallado para facilitar la depuración y el mantenimiento de la aplicación.
*   **Automatización de la Carga de Datos:**  Implementar un sistema para automatizar la carga de datos desde diferentes fuentes (CRM, sistemas de pago, etc.).
*   **Implementación de Pruebas Unitarias y de Integración:**  Desarrollar un conjunto completo de pruebas unitarias y de integración para asegurar la calidad y la estabilidad del código.

Este proyecto, aunque incompleto, sirvió como una valiosa exploración del potencial de los grafos de conocimiento para el análisis de interacciones con clientes y proporcionó información valiosa para