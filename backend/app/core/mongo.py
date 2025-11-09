import json
import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException, status

class MongoSettings():
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = 'SocialJAM'

settings = MongoSettings()

client: AsyncIOMotorClient = None
db = None
mongo_connected = False

async def connect_mongo():
    global client, db, mongo_connected
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        # Test the connection
        await db.command('ping')
        mongo_connected = True
        return True
    except Exception as e:
        print(f"Aviso: Não foi possível conectar ao MongoDB: {e}")
        print("Servidor iniciará sem funcionalidade MongoDB")
        mongo_connected = False
        client = None
        db = None
        return False

async def disconnect_mongo():
    global client, mongo_connected
    if client:
        client.close()
    mongo_connected = False

def get_mongo_db():
    if not mongo_connected or db is None:
        return None
    return db

def is_mongo_connected():
    return mongo_connected

def get_mongo_db_with_check():
    """Dependency that verifies if mongoDB is connected"""
    if not is_mongo_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço MongoDB indisponível. Funcionalidade de posts não está disponível."
        )
    return get_mongo_db()

async def apply_schemas():
    if not mongo_connected or db is None:
        print("Aviso: Schemas do MongoDB não aplicados - MongoDB não conectado")
        return
    
    try:
        # Defining path to the schemas dir
        CORE_DIR = os.path.dirname(__file__)
        BACKEND_DIR = os.path.abspath(os.path.join(CORE_DIR, ".."))
        POST_SCHEMA_PATH = os.path.join(BACKEND_DIR, "schemas", "post_schema.json")

        with open(POST_SCHEMA_PATH, 'r', encoding='utf-8') as f:
            post_schema = json.load(f)

        await db.command({
            'collMod': 'Posts',
            'validator': post_schema,
            'validationLevel': 'strict'
        })

        print('Schemas aplicados ao mongoDB')
    except Exception as e:
        print(f"Aviso: Erro ao aplicar schemas: {e}")