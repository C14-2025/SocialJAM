from app.core.mongo import db
from bson import ObjectId
from datetime import datetime, timezone

class CommentsRepo:
    async def create_comment(comment_data: dict):
        comment_data['created_at'] = datetime.now(timezone.utc)
        result = await db['Comments'].insert_one(comment_data)
        return str(result.inserted_id)

    # return the comments from a post with pagination using the post id
    async def get_post_comments(post_id: str, pagination: int = 20):
        comments = db['Comments'].find({'post_id': ObjectId(post_id)}).sort('created_at', -1)
        return await comments.to_list(length=pagination)