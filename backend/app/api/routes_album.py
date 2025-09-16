from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional
from .. import models_sql
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..repositories import album

router = APIRouter(
    tags=['Album'],
    prefix="/album"
)

@router.post('/create',status_code=status.HTTP_201_CREATED)
def createAlbum(request:schemas.Album, db:Session=Depends(get_db)):
    return album.create_album(request, db)

@router.get("/{nome}", status_code=status.HTTP_200_OK, response_model=List[schemas.Album])
def showAlbum(nome, response:Response, limit:Optional[int] = None, db:Session=Depends(get_db)):
    return album.show_album(nome, db, limit)