import json
import os
from motor.motor_asyncio import AsyncIOMotorClient

class MongoSettings():
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = 'SocialJAM'

settings = MongoSettings()

client: AsyncIOMotorClient = None
db = None

async def connect_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

async def disconnect_mongo():
    global client
    client.close()

def get_mongo_db():
    if db is None:
        raise RuntimeError('MongoDB ainda não conectado!')
    return db

async def apply_schemas():
    
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