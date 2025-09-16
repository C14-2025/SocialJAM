from sqlalchemy.orm import Session
from .. import models_sql
from ..database import get_db
from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List, Optional

def get_all(db:Session=Depends(get_db)):
    users = db.query(models_sql.User).all()
    return users

def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username).first()
    return user

def create_user(request_user: models_sql.User, db: Session = Depends(get_db)):
    new_user = models_sql.User(
        nome=request_user.nome,
        username=request_user.username,
        email=request_user.email,
        senha=request_user.senha
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

def update_user(username: str, request: models_sql.User, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} não foi encontrado")
    user.update(request.model_dump(exclude_unset=True))
    db.commit()
    return "User Updated"

def show_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models_sql.User).filter(models_sql.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe usuário {username}')
    return user