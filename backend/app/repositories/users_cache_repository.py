from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
class UserCacheRepo:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    # update a user cache or create if there is no cache for this user
    async def upsert_user_cache(self, user_id: int, name: str, user_photo_url: str = None):
        await self.db['Users_cache'].update_one(
            {'_id': user_id},
            {'$set': {'name': name, 'user_photo_url': user_photo_url, 'updated_at': datetime.now(timezone.utc)}},
            upsert=True
        )

    async def get_user_cache(self, user_id: int):
        return await self.db['Users_cache'].find_one({'_id': user_id})