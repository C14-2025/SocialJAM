from fastapi import APIRouter, Depends, HTTPException, status
from app.models.mongo_posts import PostCreate, PostDB, CommentCreate, CommentDB
from app.core.mongo import get_mongo_db, is_mongo_connected
from app.repositories.posts_repository import PostsRepo, PostNotFoundError
from app.repositories.comments_repository import CommentsRepo, CommentNotFoundError
from bson.errors import InvalidId

router = APIRouter(prefix='/posts', tags=['Posts'])

def get_mongo_db_with_check():
    """Dependency that verifies if mongoDB is connected"""
    if not is_mongo_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço MongoDB indisponível. Funcionalidade de posts não está disponível."
        )
    return get_mongo_db()

@router.get('/', response_model=list[PostDB])
async def get_last_posts(pagination: int = 20, db = Depends(get_mongo_db_with_check)):
    repo = PostsRepo(db)
    posts = await repo.get_post_list(pagination)
    return posts


@router.post('/create')
async def create_post(post: PostCreate, db = Depends(get_mongo_db_with_check)):
    repo = PostsRepo(db)
    try:
        created = await repo.create_post(post)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    return created

@router.get('/{post_id}', response_model=PostDB)
async def get_post(post_id: str, db = Depends(get_mongo_db_with_check)):
    repo = PostsRepo(db)
    try:
        post = await repo.get_post_by_id(post_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )

    return post

@router.post('/{post_id}/like')
async def like_post(post_id: str, current_user: dict, db = Depends(get_mongo_db_with_check)):
    repo = PostsRepo(db)
    try:
        await repo.like_post(post_id, current_user['id'])
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    return {'message': 'Post liked successfully'}

@router.delete('/delete/{post_id}', status_code=204)
async def delete_post(post_id: str, db = Depends(get_mongo_db_with_check)):
    repo = PostsRepo(db)
    comments_repo = CommentsRepo(db)
    try:
        result = await repo.delete_post(post_id)
        # delete every comment associated with this post
        deleted_comments = await comments_repo.on_post_deleted(post_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    except PostNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    return {
        'message': 'Post deleted successfully',
        'deletedComments': deleted_comments
    }
    
# comments related routes
@router.post('/comment')
async def create_comment(comment: CommentCreate, db = Depends(get_mongo_db_with_check)):
    repo = CommentsRepo(db)
    try:
        created = await repo.create_comment(comment)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    return created

@router.get('/comment/{comment_id}', response_model=CommentDB)
async def get_comment(comment_id: str, db = Depends(get_mongo_db_with_check)):
    repo = CommentsRepo(db)
    try:
        comment = await repo.get_comment_by_id(comment_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    except CommentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )

    return comment

@router.post('/comment/{comment_id}/like')
async def like_post(comment_id: str, current_user: dict, db = Depends(get_mongo_db_with_check)):
    repo = CommentsRepo(db)
    try:
        await repo.like_comment(comment_id, current_user['id'])
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    except CommentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    return {'message': 'Comment liked successfully'}

@router.get('/{post_id}/comments', response_model=list[CommentDB])
async def get_post_comments(post_id: str, pagination: int = 20, db = Depends(get_mongo_db_with_check)):
    repo = CommentsRepo(db)
    try:
        comments = await repo.get_post_comments(post_id, pagination)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    return comments

@router.delete('/delete/comment/{comment_id}', status_code=204)
async def delete_post(comment_id: str, db = Depends(get_mongo_db_with_check)):
    repo = CommentsRepo(db)
    try:
        result = await repo.delete_comment(comment_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    except CommentNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )



