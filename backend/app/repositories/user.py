from sqlalchemy.orm import Session
from .. import models_sql, schemas
from ..database import get_db
from fastapi import Depends, status, HTTPException
from ..core.security import Hash

def get_all_users(db:Session=Depends(get_db)):
    users = db.query(models_sql.User).all()
    return users

def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username).first()
    return user

def create_user(request_user: schemas.User, db: Session = Depends(get_db)):
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
    return new_user

def delete_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado")
    user.delete(synchronize_session=False)
    db.commit()
    return f"{username} deletado"

def update_user(username: str, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} não foi encontrado")
    
    # Hash da senha se ela foi fornecida na atualização
    update_data = request.model_dump(exclude_unset=True)
    if 'senha' in update_data:
        update_data['senha'] = Hash.hashPWD(update_data['senha'])
    
    user.update(update_data)
    db.commit()
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