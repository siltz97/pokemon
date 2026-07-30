import os
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Pokémon Collector API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pokemon_router = APIRouter(prefix="/api/pokemon", tags=["pokemon"])
collection_router = APIRouter(prefix="/api/collection", tags=["collection"])

class CreatePokemon(BaseModel):
    nome: str
    tipo: str
    immagine_url: str = ""
    numero: int

@pokemon_router.get("/")
async def list_pokemon():
    response = supabase.table("pokemon").select("*").order("numero").execute()
    return response.data

@pokemon_router.get("/{pokemon_id}")
async def get_pokemon(pokemon_id: int):
    response = supabase.table("pokemon").select("*").eq("id", pokemon_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Pokémon non trovato")
    return response.data[0]

@pokemon_router.post("/")
async def create_pokemon(pokemon: CreatePokemon):
    existing = supabase.table("pokemon").select("*").eq("numero", pokemon.numero).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="Numero Pokédex già esistente")
    response = supabase.table("pokemon").insert({
        "nome": pokemon.nome,
        "tipo": pokemon.tipo,
        "immagine_url": pokemon.immagine_url,
        "numero": pokemon.numero,
    }).execute()
    return response.data[0]

@collection_router.get("/")
async def get_collection():
    response = supabase.table("pokemon").select("*").eq("catturato", True).order("numero").execute()
    return response.data

@collection_router.post("/catch/{pokemon_id}")
async def catch_pokemon(pokemon_id: int):
    existing = supabase.table("pokemon").select("*").eq("id", pokemon_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Pokémon non trovato")
    response = supabase.table("pokemon").update({"catturato": True}).eq("id", pokemon_id).execute()
    return response.data[0] if response.data else {"message": "Pokémon catturato!"}

@collection_router.delete("/release/{pokemon_id}")
async def release_pokemon(pokemon_id: int):
    existing = supabase.table("pokemon").select("*").eq("id", pokemon_id).execute()
    if not existing.data:
        raise HTTPException(status_code=404, detail="Pokémon non trovato")
    response = supabase.table("pokemon").update({"catturato": False}).eq("id", pokemon_id).execute()
    return response.data[0] if response.data else {"message": "Pokémon rilasciato!"}

app.include_router(pokemon_router)
app.include_router(collection_router)
