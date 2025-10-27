from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.mongo_users import UserCache
class UserCacheRepo:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    # update a user cache or create if there is no cache for this user
    async def upsert_user_cache(self, user: UserCache):
        result = await self.db['Users_cache'].update_one(
            {'_id': user.id},
            {'$set': {'name': user.name, 'user_photo_url': user.user_photo_url, 'updated_at': datetime.now(timezone.utc)}},
            upsert=True
        )
        return result.upserted_id

    async def get_user_cache_by_id(self, user_id: int):
        user = await self.db['Users_cache'].find_one({'_id': user_id})
        if not user:
            raise UserCacheNotFoundError(user_id)
        
        return user

class UserCacheNotFoundError(Exception):
    # Trhows this error when a user cant be found on the data base
    def __init__(self, user_id: str):
        super().__init__(f'Usuario com ID {user_id} não encontrado no cache.')