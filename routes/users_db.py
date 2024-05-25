# USERS DB API
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb", 
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})

@router.get("/",response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# llamado por path
@router.get("/{id}")
async def user(id:str):
    return buscarUser("_id",ObjectId(id))
    
# llamado por query
@router.get("/")
async def user(id:str):
    return buscarUser("_id",ObjectId(id))

# POST Para crear usuario
@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def crearuser(user:User): #recibimos parametro user de tipo User que fue la entidad que creamos
    if type(buscarUser("email",user.email))==User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='El usuario ya existe')
    
    user_dict = user.model_dump(exclude_unset=True)
    if "id" in user_dict:
        del user_dict["id"]  # Eliminamos id si está presente
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))
    return User(**new_user)

# PUT Para actualiza usuario
@router.put("/",response_model=User)
async def modificaruser(user:User): #recibimos parametro user de tipo User que fue la entidad que creamos
    
    user_dict=dict(user)
    del user_dict["id"] 
    print('que paso')
    try:        
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
    except:
        return {"error":"No se ha actualizado el usuario"}
            
    return buscarUser("_id",ObjectId(user.id))

# DELETE
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def eliminaruser(id:str):
    usuarioEncontrado=db_client.users.find_one_and_delete({"_id":ObjectId(id)})
 
    if not usuarioEncontrado:
        return {"error":"No se ha eliminado nada"}


def buscarUser(field:str,key):
    
    try:
       usuario= db_client.users.find_one({field:key})
       return User(**user_schema(usuario))
    except:
        return {"error":"No se encuentra usuario"}
    
