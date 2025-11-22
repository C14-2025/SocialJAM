from fastapi import APIRouter, Depends, status, Response, HTTPException, File, UploadFile
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.mongo import get_mongo_db_with_check
from typing import List, Annotated
from ..repositories import user
from ..oauth2 import get_current_user
from ..services.spotify_service import spotify_service
from .. import models_sql
import os


router = APIRouter(
    tags=['User'],
    prefix="/user"
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
async def createUser(request_user:schemas.User, db:Session = Depends(get_db), mongo = Depends(get_mongo_db_with_check)):
    return await user.create_user(request_user, db, mongo)

@router.delete('/{username}/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode deletar sua própria conta, animal"
        )
    return user.delete_user(username, db)

@router.put('/{username}/update', status_code=status.HTTP_202_ACCEPTED)
async def update_user(username, request:schemas.User, db:Session=Depends(get_db), mongo = Depends(get_mongo_db_with_check), current_user=Depends(get_current_user)):
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode atualizar sua própria conta, animal"
        )
    return await user.update_user(username, request, db, mongo)

@router.get('/', response_model=List[schemas.ShowUser])
def get_all_users(db:Session = Depends(get_db), current_user=Depends(get_current_user)):
    return user.get_all_users(db)

@router.get('/me', status_code=200, response_model=schemas.ShowUser)
async def get_current_user_info(
    current_user=Depends(get_current_user),
    mongo = Depends(get_mongo_db_with_check)
):
    from ..repositories.users_cache_repository import UserCacheRepo
    
    # Buscar mongo_id do usuário
    cache_repo = UserCacheRepo(mongo)
    try:
        mongo_id = await cache_repo.get_mongo_id_by_sql_id(current_user.id)
    except:
        mongo_id = None
    
    # Criar resposta com mongo_id
    user_dict = {
        "id": current_user.id,
        "username": current_user.username,
        "nome": current_user.nome,
        "email": current_user.email,
        "user_photo_url": current_user.user_photo_url,
        "favorite_artist": current_user.favorite_artist,
        "spotify_user_token": current_user.spotify_user_token,
        "mongo_id": mongo_id
    }
    
    return user_dict

@router.put('/me/favorite-artist', status_code=200, response_model=schemas.ShowUser)
def set_favorite_artist(
    artist_data: schemas.FavoriteArtist,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Define o artista favorito do usuário usando o ID do Spotify"""
    
    # Busca informações do artista no Spotify
    artist_info = spotify_service.get_artist_info(artist_data.artist_id)
    
    if not artist_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artista não encontrado no Spotify"
        )
    
    # Atualiza o artista favorito do usuário
    updated_user = user.update_favorite_artist(
        username=current_user.username,
        artist_name=artist_info["name"],
        db=db
    )
    
    return updated_user

@router.get('/id/{user_id}', status_code=200, response_model=schemas.ShowUser)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_data = user.get_user_by_id(user_id, db)
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user_data

@router.get('/{username}', status_code=200, response_model=schemas.ShowUser)
def show_user(username,response:Response, db:Session=Depends(get_db)):
    return user.show_user(username, db)

@router.post('/upload-photo', status_code=200)
async def upload_profile_picture(
    file: Annotated[UploadFile, File()],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    filename = file.filename
    content_type = file.content_type

    contents = await file.read()

    if not os.path.exists(f'images/pfp/{current_user.username}'):
        os.makedirs(f'images/pfp/{current_user.username}')

    with open(f'images/pfp/{current_user.username}/{filename}', 'wb') as f:
        f.write(contents)


    file_url = f'backend/images/pfp/{current_user.username}/{filename}'
    # Atualiza a URL da foto do usuário no banco de dados
    user_record = db.query(models_sql.User).filter(models_sql.User.id == current_user.id).first()
    user_record.user_photo_url = file_url  # Aqui você pode usar uma URL pública se estiver usando um serviço de armazenamento
    db.commit()
    db.refresh(user_record)

    return {"filename": filename, "content_type": content_type, "message": "Upload successful"}

@router.get('/pesquisar/{input}', status_code=200, response_model=List[schemas.ShowUser])
def search_users(input: str, db:Session=Depends(get_db)):
    users = db.query(models_sql.User).filter(models_sql.User.username.ilike(f"{input}%")).all()
    return users