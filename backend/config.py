import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USER = os.environ.get("NEO4J_USER")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
OPEN_API_KEY = os.environ.get("OPEN_API_KEY")

if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, OPEN_API_KEY]):
    raise ValueError(
        "NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD deben estar definidos en .env"
    )
