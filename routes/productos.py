from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/productos", 
                   tags=["productos"],
                   responses={404:{"message":"No encontrado"}})

lista_productos=["p1", "p2", "p3"]


@router.get("/")
async def productos():
    return lista_productos

@router.get("/{id}")
async def producto(id:int):
    return lista_productos[id]