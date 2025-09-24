from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timezone
from app.models.mongo_posts import CommentCreate
from app.repositories.posts_repository import PostsRepo

class CommentsRepo:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_comment(self, comment: CommentCreate):
        post_repo = PostsRepo(self.db)
        await post_repo.get_post_by_id(comment.post_id)

        comment_data = {
            'post_id': ObjectId(comment.post_id),
            'author_id': ObjectId(comment.author_id),
            'content': comment.content,
            'likes': 0,
            'liked_by': [],
            'created_at': datetime.now(timezone.utc),
        }
        result = await self.db['Comments'].insert_one(comment_data)
        return str(result.inserted_id)

    async def get_comment_by_id(self, comment_id: str):
        comment = await self.db['Comments'].find_one({'_id': ObjectId(comment_id)})
        if not comment:
            raise CommentNotFoundError(comment_id)
        else:
            comment['_id'] = str(comment['_id'])
            comment['post_id'] = str(comment['post_id'])
            comment['author_id'] = str(comment['author_id'])
        return comment
    
    async def like_comment(self, comment_id: str, user_id: str):
        result = await self.db['Comments'].update_one(
            {'_id': ObjectId(comment_id)},
            {'$addToSet': {'liked_by': ObjectId(user_id)}, '$inc': {'likes': 1}}
        )

        if result.modified_count < 1:
            raise CommentNotFoundError(comment_id)

    # return the comments from a post with pagination using the post id
    async def get_post_comments(self, post_id: str, pagination: int = 20):
        comments = self.db['Comments'].find({'post_id': ObjectId(post_id)}).sort('created_at', -1)
        comments = await comments.to_list(length=pagination)
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            comment['post_id'] = str(comment['post_id'])
            comment['author_id'] = str(comment['author_id'])
            users = []
            for user in comment['liked_by']:
                users.append(str(user))
            comment['liked_by'] = users
        return comments
    
    async def delete_comment(self, comment_id: str):
        result = await self.db['Comments'].delete_one({'_id': ObjectId(comment_id)})
        if result.deleted_count < 1:
            raise CommentNotFoundError(comment_id)
        
        return result.deleted_count
    # this function is responsible for deleting every comment associated with a post that was deleted
    async def on_post_deleted(self, post_id: str):
        result = await self.db['Comments'].delete_many(
            {'post_id': ObjectId(post_id)}
        )
        return result.deleted_count

class CommentNotFoundError(Exception):
    # Trhows this error when a comment cant be found on the data base
    def __init__(self, comment_id: str):
        super().__init__(f'Comentario com ID {comment_id} não foi encontrado.')