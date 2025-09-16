from fastapi import APIRouter, Depends, HTTPException, status
from app.models.mongo_posts import PostCreate, PostDB
from app.core.mongo import get_mongo_db
from app.repositories.posts_repository import PostsRepo
from datetime import datetime, timezone
from bson.errors import InvalidId

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=list[PostDB])
async def get_last_posts(pagination: int = 20, db = Depends(get_mongo_db)):
    repo = PostsRepo(db)
    posts = await repo.get_post_list(pagination)
    return posts


@router.post('/create')
async def create_post(post: PostCreate, db = Depends(get_mongo_db)):
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
async def get_post(post_id: str, db = Depends(get_mongo_db)):
    repo = PostsRepo(db)
    try:
        post = await repo.get_post_by_id(post_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid ID format'
        )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    return post

@router.post('/{post_id}/like')
async def like_post(post_id: str, current_user: dict, db = Depends(get_mongo_db)):
    repo = PostsRepo(db)
    post = await repo.get_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    await repo.like_post(post_id, current_user['id'])
    return {'message': 'Post liked successfully'}

@router.delete('/delete/{post_id}', status_code=204)
async def delete_post(post_id: str, db = Depends(get_mongo_db)):
    repo = PostsRepo(db)
    result = await repo.delete_post(post_id)
    if result == 0:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
