# Este fichero va a gestionar la conexion a nuestra base de datos con mongo 

from pymongo import MongoClient

# db_client=MongoClient().local
#con esto instanciamos la clase mongo_clienty la guardamos

# Remoto
db_client=MongoClient(
    "mongodb+srv://test:test@cluster0.l8x0t0q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test