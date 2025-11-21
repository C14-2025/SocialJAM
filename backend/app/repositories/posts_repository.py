from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timezone
from app.models.mongo_posts import PostCreate

class PostsRepo:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_post(self, post: PostCreate):
        post_data = {
            'author_id': ObjectId(post.author_id),  # Converte string do MongoDB ObjectId para ObjectId
            'artist_id': post.artist_id,  # ID do Spotify (string)
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
        """Busca lista de posts com informações do autor"""
        pipeline = [
            {'$sort': {'created_at': -1}},
            {'$limit': pagination},
            {
                '$lookup': {
                    'from': 'Users_cache',
                    'localField': 'author_id',
                    'foreignField': '_id',
                    'as': 'author_info'
                }
            },
            {
                '$unwind': {
                    'path': '$author_info',
                    'preserveNullAndEmptyArrays': True
                }
            }
        ]
        
        posts = await self.db['Posts'].aggregate(pipeline).to_list(length=pagination)
        
        for post in posts:
            post['_id'] = str(post['_id'])
            post['author_id'] = str(post['author_id'])
            
            # Adicionar informações do autor
            if 'author_info' in post and post['author_info']:
                post['author'] = {
                    'name': post['author_info'].get('name', 'Usuário'),
                    'user_photo_url': post['author_info'].get('user_photo_url', None)
                }
                del post['author_info']
            else:
                post['author'] = {
                    'name': 'Usuário',
                    'user_photo_url': None
                }
            
            # Converter liked_by para strings
            users = []
            for user in post.get('liked_by', []):
                users.append(str(user))
            post['liked_by'] = users
            
        return posts
    
    async def delete_post(self, post_id: str):
        result = await self.db['Posts'].delete_one({'_id': ObjectId(post_id)})
        if result.deleted_count < 1:
            raise PostNotFoundError(post_id)
        
        return result.deleted_count
    
    async def get_posts_by_artist(self, artist_id: str, pagination: int = 20):
        """Busca posts de um artista específico pelo ID do Spotify com informações do autor"""
        pipeline = [
            {'$match': {'artist_id': artist_id}},
            {'$sort': {'created_at': -1}},
            {'$limit': pagination},
            {
                '$lookup': {
                    'from': 'Users_cache',
                    'localField': 'author_id',
                    'foreignField': '_id',
                    'as': 'author_info'
                }
            },
            {
                '$unwind': {
                    'path': '$author_info',
                    'preserveNullAndEmptyArrays': True
                }
            }
        ]
        
        posts = await self.db['Posts'].aggregate(pipeline).to_list(length=pagination)
        
        print(f"DEBUG: Encontrados {len(posts)} posts para o artista {artist_id}")
        
        for post in posts:
            print(f"DEBUG: Post {post.get('_id')} - author_info: {post.get('author_info', 'NONE')}")
            
            post['_id'] = str(post['_id'])
            post['author_id'] = str(post['author_id'])
            
            # Adicionar informações do autor
            if 'author_info' in post and post['author_info']:
                post['author'] = {
                    'name': post['author_info'].get('name', 'Usuário'),
                    'user_photo_url': post['author_info'].get('user_photo_url', None)
                }
                del post['author_info']
                print(f"DEBUG: Autor populado: {post['author']}")
            else:
                post['author'] = {
                    'name': 'Usuário',
                    'user_photo_url': None
                }
                print(f"DEBUG: Sem author_info, usando padrão")
            
            # Converter liked_by para strings
            users = []
            for user in post.get('liked_by', []):
                users.append(str(user))
            post['liked_by'] = users
            
        return posts
    
class PostNotFoundError(Exception):
    # Trhows this error when a post cant be found on the data base
    def __init__(self, post_id: str):
        super().__init__(f'Post com ID {post_id} não foi encontrado.')