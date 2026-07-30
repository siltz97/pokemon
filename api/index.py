import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import pokemon, collection

app = FastAPI(title="Pokémon Collector API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pokemon.router, prefix="/api/pokemon", tags=["pokemon"])
app.include_router(collection.router, prefix="/api/collection", tags=["collection"])
