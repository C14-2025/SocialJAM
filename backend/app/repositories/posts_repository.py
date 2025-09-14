from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client['SocialJAM']

class PostsRepo:

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db

    async def create_post(self, post_data: dict):
        post_data['likes'] = 0
        post_data['liked_by'] = []
        post_data['created_at'] = datetime.now(timezone.utc)
        result = await self.db['Posts'].insert_one(post_data)
        return str(result.inserted_id)

    async def get_post_by_id(self, post_id: str):
        post = await self.db['Posts'].find_one({'_id': ObjectId(post_id)})
        if post:
            post['_id'] = str(post['_id'])
        return post

    async def like_post(self, post_id: str, user_id: int):
        await self.db['Posts'].update_one(
            {'_id': ObjectId(post_id)},
            {'$addToSet': {'liked_by': user_id}, '$inc': {'likes': 1}}
        )

    async def get_post_list(self, pagination: int = 20):
        # get a list of posts sorted by created_at with a pagination limit
        posts = await self.db['Posts'].find().sort('created_at', -1).limit(pagination).to_list(length=pagination)
        return [{**p, '_id': str(p['_id'])} for p in posts]
    
    async def delete_post(self, post_id: str):
        result = await db['Posts'].delete_one({'_id': ObjectId(post_id)})
        return result.deleted_count