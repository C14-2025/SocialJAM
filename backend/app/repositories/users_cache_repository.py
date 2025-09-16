from datetime import datetime, timezone
from app.core.mongo import db

class UserCacheRepo:
    # update a user cache or create if there is no cache for this user
    async def upsert_user_cache(user_id: int, name: str, user_photo_url: str = None):
        await db['Users_cache'].update_one(
            {'_id': user_id},
            {'$set': {'name': name, 'user_photo_url': user_photo_url, 'updated_at': datetime.now(timezone.utc)}},
            upsert=True
        )

    async def get_user_cache(user_id: int):
        return await db['Users_cache'].find_one({'_id': user_id})