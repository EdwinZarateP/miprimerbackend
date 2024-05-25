from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


router = APIRouter(prefix="/basicauth", 
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})
# con esto arranca el servidor: uvicorn autenticacion_basica:app --reload

oauth2=OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username:str
    full_name:str
    email:str
    disable:bool

class UserDB(User):
    clave:str

base_usuarios={# esto un diccionario que contiene datos de usuarios,
    # donde la clave es el nombre de usuario y el valor es
    # otro diccionario con la información del usuario.
    "edwin":{
        "username":"Edwin",
        "full_name":"Edwin Zarate",
        "email":"emzp",
        "disable":True,
        "clave":"123"
    },
    "laura":{
        "username":"Laura",
        "full_name":"Laura Navarro",
        "email":"lvno",
        "disable":False,
        "clave":"1234"
    }
}

def buscarusuario(username:str):
    if username in base_usuarios: #Esta línea verifica si el username (nombre de usuario proporcionado) existe como una clave en el diccionario base_usuarios
        return User(**base_usuarios[username])#Si el nombre de usuario existe en
        # base_usuarios, se crea y retorna una instancia de la clase UserDB utilizando
        # los datos correspondientes al usuario. La clase UserDB es una extensión de 
        # la clase User e incluye todos los campos de User más el campo clave.
        # por otro lado base_usuarios[username] recupera el diccionario de datos del usuario
        # correspondiente al username.

def buscarusuarioDB(username:str):
    if username in base_usuarios: #Esta línea verifica si el username (nombre de usuario proporcionado) existe como una clave en el diccionario base_usuarios
        return UserDB(**base_usuarios[username])

     
async def usuario_actual(token:str=Depends(oauth2)):
    usuario=buscarusuario(token)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Credenciales invalidas',
                            headers={"WWW-Authenticate":"Bearer"})
    if usuario.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Usuario inactivo')
    return usuario

    
@router.post("/login")
async def login(form:OAuth2PasswordRequestForm=Depends()):
    usuario_bd=base_usuarios.get(form.username) #.get(form.username) es un método de diccionario
    # en Python que intenta obtener el valor asociado con la clave form.username en el diccionario base_usuarios.
    if not usuario_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='El usuario no es correcto')
    
    usuario = buscarusuarioDB(form.username)
    if not form.password==usuario.clave:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='la clave no es correcta')

    return {"access_token": usuario.username,"token_type":"bearer"}


@router.get("/usuarios/yo")
async def yo(usuario:User=Depends(usuario_actual)):  
    return usuario