from fastapi import APIRouter, Depends, status, Response
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..repositories import user


router = APIRouter(
    tags=['User'],
    prefix="/user"
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def createUser(request_user:schemas.User, db:Session = Depends(get_db)):
    return user.create_user(request_user, db)

@router.delete('/{username}/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username, db:Session=Depends(get_db)):
    return user.delete_user(username, db)

@router.put('/{username}/update', status_code=status.HTTP_202_ACCEPTED)
def update_user(username, request:schemas.User, db:Session=Depends(get_db)):
    return user.update_user(username, request, db)

@router.get('/', response_model=List[schemas.ShowUser])
def get_all_users(db:Session = Depends(get_db)):
    return user.get_all(db)

@router.get('/{username}', status_code=200, response_model=schemas.ShowUser)
def show_user(username,response:Response, db:Session=Depends(get_db)):
    return user.show_user(username, db)