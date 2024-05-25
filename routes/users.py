from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["usuarios"],
                   responses={404:{"message":"No encontrado"}})
# con esto arranca el servidor uvicorn users:app --reload

# vamos a crear la entidad usuario 
class User(BaseModel): #aca ponemos el BaseModel para crear la entidad
    id:int
    name:str
    surname:str
    url:str
    edad:int

# vamos a darle valores a la entidad usuario 

lista_usuarios=[User(id=1,name="Edwin",surname="zarate", url="emzp1994@gmail.com",edad=30),
                User(id=2,name="Laura",surname="navarro", url="laura@gmail.com",edad=26)]

@router.get("/users")
async def users():
    return lista_usuarios

# llamado por path
@router.get("/user/{id}")
async def user(id:int):
    return buscarUser(id)
    
# llamado por query
@router.get("/user/")
async def user(id:int):
    return buscarUser(id)

# POST Para crear usuario
@router.post("/crearuser/",response_model=User, status_code=201)
async def crearuser(user:User): #recibimos parametro user de tipo User que fue la entidad que creamos
    if type(buscarUser(user.id))==User:
        raise HTTPException(status_code=404,detail='El usuario ya existe')
    else:
        lista_usuarios.append(user)
        return user

# PUT Para actualiza usuario
@router.put("/modificaruser/")
async def modificaruser(user:User): #recibimos parametro user de tipo User que fue la entidad que creamos
    usuarioEncontrado=False
    for index, usuarioGuardado in enumerate(lista_usuarios): #Este bucle recorre lista_usuarios, una lista que contiene objetos de tipo User, Utiliza enumerate para obtener tanto el índice (index) como el usuario guardado (usuarioGuardado) en cada iteración.
        if usuarioGuardado.id == user.id:
            lista_usuarios[index]=user #Si los id coinciden, se actualiza el usuario en la lista en la posición index con el nuevo user proporcionado
            usuarioEncontrado=True
    if not usuarioEncontrado:
        return {"error":"No se ha actualizado el usuario"}
    else:
        return user

# DELETE
@router.delete("/eliminaruser/{id}")
async def eliminaruser(id:int):
    usuarioEncontrado=False
    for index, usuarioGuardado in enumerate(lista_usuarios): #Este bucle recorre lista_usuarios, una lista que contiene objetos de tipo User, Utiliza enumerate para obtener tanto el índice (index) como el usuario guardado (usuarioGuardado) en cada iteración.
        if usuarioGuardado.id == id:
            del lista_usuarios[index] #Este metodo del elimina el usuario que contenga el id
            usuarioEncontrado=True
    if not usuarioEncontrado:
        return {"error":"No se ha eliminado el usuario"}
    else:
        return {"Exito":"Se ha eliminado el usuario"}

def buscarUser(id:int):
    # filter filtra la lista_usuarios para obtener aquellos cuyo id coincide con id que estamos ingresando
    usuarios = filter(lambda user:user.id==id,lista_usuarios) 
    try:
        return list(usuarios)[0]
    except:
        return {"error":"No se encuentra usuario"}
    
