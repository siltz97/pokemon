from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Pokemon(BaseModel):
    id: int
    numero: int
    nome: str
    tipo: str
    immagine_url: Optional[str] = None
    catturato: bool = False
    created_at: Optional[datetime] = None
