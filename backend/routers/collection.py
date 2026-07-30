from fastapi import APIRouter, HTTPException
from database import supabase

router = APIRouter()

@router.get("/")
async def get_collection():
    response = (
        supabase.table("pokemon")
        .select("*")
        .eq("catturato", True)
        .order("numero")
        .execute()
    )
    return response.data

@router.post("/catch/{pokemon_id}")
async def catch_pokemon(pokemon_id: int):
    existing = (
        supabase.table("pokemon")
        .select("*")
        .eq("id", pokemon_id)
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=404, detail="Pokémon non trovato")

    response = (
        supabase.table("pokemon")
        .update({"catturato": True})
        .eq("id", pokemon_id)
        .execute()
    )
    return response.data[0] if response.data else {"message": "Pokémon catturato!"}

@router.delete("/release/{pokemon_id}")
async def release_pokemon(pokemon_id: int):
    existing = (
        supabase.table("pokemon")
        .select("*")
        .eq("id", pokemon_id)
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=404, detail="Pokémon non trovato")

    response = (
        supabase.table("pokemon")
        .update({"catturato": False})
        .eq("id", pokemon_id)
        .execute()
    )
    return response.data[0] if response.data else {"message": "Pokémon rilasciato!"}
