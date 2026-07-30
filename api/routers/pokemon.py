from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import supabase

router = APIRouter()

class CreatePokemon(BaseModel):
    nome: str
    tipo: str
    immagine_url: str = ""
    numero: int

@router.get("/")
async def list_pokemon():
    response = supabase.table("pokemon").select("*").order("numero").execute()
    return response.data

@router.get("/{pokemon_id}")
async def get_pokemon(pokemon_id: int):
    response = (
        supabase.table("pokemon")
        .select("*")
        .eq("id", pokemon_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Pokémon non trovato")
    return response.data[0]

@router.post("/")
async def create_pokemon(pokemon: CreatePokemon):
    existing = (
        supabase.table("pokemon")
        .select("*")
        .eq("numero", pokemon.numero)
        .execute()
    )
    if existing.data:
        raise HTTPException(status_code=409, detail="Numero Pokédex già esistente")

    response = (
        supabase.table("pokemon")
        .insert({
            "nome": pokemon.nome,
            "tipo": pokemon.tipo,
            "immagine_url": pokemon.immagine_url,
            "numero": pokemon.numero,
        })
        .execute()
    )
    return response.data[0]
