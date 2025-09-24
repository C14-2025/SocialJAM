from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timezone
from app.models.mongo_posts import PostCreate

class PostsRepo:

    def __init__(self, db: AsyncIOMotorDatabase):
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
        if not post:
            raise PostNotFoundError(post_id)
        else:
            post['_id'] = str(post['_id'])
        return post

    async def like_post(self, post_id: str, user_id: str):
        result = await self.db['Posts'].update_one(
            {'_id': ObjectId(post_id)},
            {'$addToSet': {'liked_by': ObjectId(user_id)}, '$inc': {'likes': 1}}
        )

        if result.modified_count < 1:
            raise PostNotFoundError(post_id)

    async def get_post_list(self, pagination: int = 20):
        # get a list of posts sorted by created_at with a pagination limit
        posts = await self.db['Posts'].find().sort('created_at', -1).limit(pagination).to_list(length=pagination)
        for post in posts:
            post['_id'] = str(post['_id'])
            post['author_id'] = str(post['author_id'])
            users = []
            for user in post['liked_by']:
                users.append(str(user))
            post['liked_by'] = users
        return posts
    
    async def delete_post(self, post_id: str):
        result = await self.db['Posts'].delete_one({'_id': ObjectId(post_id)})
        if result.deleted_count < 1:
            raise PostNotFoundError(post_id)
        
        return result.deleted_count
    
class PostNotFoundError(Exception):
    # Trhows this error when a post cant be found on the data base
    def __init__(self, post_id: str):
        super().__init__(f'Post com ID {post_id} não foi encontrado.')