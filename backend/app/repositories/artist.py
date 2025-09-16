from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional
from .. import models_sql
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

def create_artist(request:schemas.Artist, db:Session=Depends(get_db)):
    new_artist=models_sql.Artist(
        nome = request.nome,
        music_genre=request.music_genre
    )
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)
    return new_artist
def show_all_artists(db:Session=Depends(get_db)):
    artists = db.query(models_sql.Artist).all()
    return artists

def show_artist(nome: str, db:Session=Depends(get_db), limit:Optional[int] = None):
    query = db.query(models_sql.Artist).filter(models_sql.Artist.nome==nome)
    if limit:
        query = query.limit(limit)
    artists = query.all()
    if not artists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nao existe esse Artista")
    return artists