from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.mongo_users import UserCache
from bson import ObjectId

class UserCacheRepo:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    # update a user cache or create if there is no cache for this user
    async def upsert_user_cache(self, user: UserCache):
        result = await self.db['Users_cache'].update_one(
            {'sql_user_id': user.sql_user_id},
            {'$set': {'name': user.name, 'user_photo_url': user.user_photo_url, 'updated_at': datetime.now(timezone.utc)}},
            upsert=True
        )
        return result.upserted_id

    async def get_user_cache_by_id(self, user_id: int):
        user = await self.db['Users_cache'].find_one({'sql_user_id': user_id})
        if not user:
            raise UserCacheNotFoundError(user_id)
        
        return user
    
    async def get_mongo_id_by_sql_id(self, sql_user_id: int) -> str:
        """Retorna o ObjectId do MongoDB do usuário usando o ID do SQL"""
        user = await self.db['Users_cache'].find_one({'sql_user_id': sql_user_id})
        if not user:
            raise UserCacheNotFoundError(sql_user_id)
        
        return str(user['_id'])

class UserCacheNotFoundError(Exception):
    # Trhows this error when a user cant be found on the data base
    def __init__(self, user_id: str):
        super().__init__(f'Usuario com ID {user_id} não encontrado no cache.')