from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional
from .. import models_sql
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

def create_album(request:schemas.Album, db:Session=Depends(get_db)):
    new_album = models_sql.Album(
        nome=request.nome,
        total_tracks=request.total_tracks,
        artist_id = request.artist_id
    )
    db.add(new_album)
    db.commit()
    db.refresh(new_album)
    return new_album

def show_album(nome: str, db:Session=Depends(get_db), limit:Optional[int] = None):
    query = db.query(models_sql.Album).filter(models_sql.Album.nome==nome)
    if limit:
        query = query.limit(limit)
    albums = query.all()
    if not albums:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nao existe esse Album")
    return albums