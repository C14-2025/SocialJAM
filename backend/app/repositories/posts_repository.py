from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone
from app.models.mongo_posts import PostCreate

class PostsRepo:

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db

    async def create_post(self, post: PostCreate):
        post_data = {
            'author_id': ObjectId(post.author_id),
            'content': post.content,
            'images': post.images,
            'likes': 0,
            'liked_by': [],
            'created_at': datetime.now(timezone.utc),
        }
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
        result = await self.db['Posts'].delete_one({'_id': ObjectId(post_id)})
        return result.deleted_count