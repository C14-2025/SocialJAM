from sqlalchemy.orm import Session
from .. import models_sql, schemas
from ..database import get_db
from fastapi import Depends, status, HTTPException
from ..core.security import Hash
from app.repositories.users_cache_repository import UserCacheRepo
from app.models.mongo_users import UserCache
from app.core.mongo import get_mongo_db_with_check
from datetime import datetime

def get_all_users(db:Session=Depends(get_db)):
    users = db.query(models_sql.User).all()
    return users

def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username).first()
    return user

def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.id == user_id).first()
    return user

async def create_user(request_user: schemas.User, db: Session = Depends(get_db), mongo = Depends(get_mongo_db_with_check)):
    # mongoDB cache instance
    cache = UserCacheRepo(mongo)
    usernameaux = request_user.username
    if "@" in usernameaux:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Username não pode conter '@'")
    new_user = models_sql.User(
        nome=request_user.nome,
        username=usernameaux,
        email=request_user.email,
        senha=Hash.hashPWD(request_user.senha)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # update the users cache on mongoDB
    await cache.upsert_user_cache(
        user=UserCache(
            id="",  # Será gerado pelo MongoDB
            sql_user_id=new_user.id,
            name=new_user.nome,
            user_photo_url=new_user.user_photo_url,
            updated_at=datetime.now()
        )
    )
    return new_user

def delete_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado")
    user.delete(synchronize_session=False)
    db.commit()
    return f"{username} deletado"

async def update_user(username: str, request: schemas.User, db: Session = Depends(get_db), mongo = Depends(get_mongo_db_with_check)):
    # mongoDB cache instance
    cache = UserCacheRepo(mongo)
    user = db.query(models_sql.User).filter(models_sql.User.username == username)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} não foi encontrado")
    
    # Hash da senha se ela foi fornecida na atualização
    update_data = request.model_dump(exclude_unset=True)
    if 'senha' in update_data:
        update_data['senha'] = Hash.hashPWD(update_data['senha'])
    
    user.update(update_data)
    db.commit()
    
    # Get the updated user to refresh the cache
    updated_user = user.first()
    # update the users cache on mongoDB
    await cache.upsert_user_cache(
        user=UserCache(
            id="",  # Será mantido o existente ou gerado novo
            sql_user_id=updated_user.id,
            name=updated_user.nome,
            user_photo_url=updated_user.user_photo_url,
            updated_at=datetime.now()
        )
    )
    
    return "User Updated"

def show_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe usuário {username}')
    return user

def update_favorite_artist(username: str, artist_name: str, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário {username} não encontrado')
    
    user.favorite_artist = artist_name
    db.commit()
    db.refresh(user)
    return user

def update_spotify_tokens(user_id: int, access_token: str, refresh_token: str, expires_at: datetime, db: Session):
    user = db.query(models_sql.User).filter(models_sql.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário não encontrado')
    
    user.spotify_user_token = access_token
    if refresh_token:  
        user.spotify_refresh_token = refresh_token
    user.spotify_expires_at = expires_at
    db.commit()
    db.refresh(user)
    return user

def get_user_spotify_tokens(user_id: int, db: Session):
    user = db.query(models_sql.User).filter(models_sql.User.id == user_id).first()
    if not user:
        return None
    
    return {
        "access_token": user.spotify_user_token,
        "refresh_token": user.spotify_refresh_token,
        "expires_at": user.spotify_expires_at
    }