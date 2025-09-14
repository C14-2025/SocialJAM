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