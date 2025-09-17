from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional
from .. import models_sql, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..core.permissions import require_system_script_for_artist_creation

router = APIRouter(
    tags=['Artist'],
    prefix="/artist"
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def createArtist(
    request: schemas.Artist, 
    db: Session = Depends(get_db),
    _: None = Depends(require_system_script_for_artist_creation)
):
    # Esta rota só será executada se a verificação de permissão passar
    new_artist = models_sql.Artist(
        nome=request.nome,
        music_genre=request.music_genre
    )
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)
    return new_artist

@router.get("/all",response_model=List[schemas.Artist])
def showAllArtists(db:Session=Depends(get_db)):
    artists = db.query(models_sql.Artist).all()
    return artists

@router.get("/{nome}", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowArtist])
def showArtist(nome, response:Response, limit: Optional[int] = None, db:Session=Depends(get_db)):
    query = db.query(models_sql.Artist).filter(models_sql.Artist.nome==nome)
    if limit:
        query = query.limit(limit)
    artists = query.all()
    if not artists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nao existe esse Artista")
    return artists