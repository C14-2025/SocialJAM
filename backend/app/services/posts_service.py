from app.repositories import posts_repository, users_cache_repository
import models
# NOT WORKING OR TESTED YET
async def get_post_with_author(post_id: str, sql_session):
    post = await posts_repository.get_post_by_id(post_id)
    if not post:
        return None
    
    # try to get the user from the cache
    user_cache = await users_cache_repository.get_user_cache(post['author_id'])
    if not user_cache:
        # if the cache dosn't exists get the user from the SQL
        user = sql_session.query(models.User).filter(models.User.id == post['author_id']).first()
        if user:
            await users_cache_repository.upsert_user_cache(user.id, user.nome, user.user_photo_url)
            user_cache = {'_id': user.id, 'name': user.nome, 'user_photo_url': user.user_photo_url}
    
    return {**post, 'author': user_cache}