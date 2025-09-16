from fastapi import APIRouter, Depends
from app import schemas, database
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
async def login(request: schemas.Login, db:Session = Depends(database.get_db)):
    if db.query(schemas.User).filter(schemas.User.email == request.email).first():
        user = db.query(schemas.User).filter(schemas.User.email == request.email).first()
    if db.query(schemas.User).filter(schemas.User.username == request.email).first():
        user = db.query(schemas.User).filter(schemas.User.username == request.email).first()
    return {"message": "Login endpoint"}