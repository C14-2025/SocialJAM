from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, database, models_sql, JWT_token
from sqlalchemy.orm import Session
from ..core.security import Hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    if "@" in request.username:
        # Login por email
        user = db.query(models_sql.User).filter(models_sql.User.email == request.username).first()
    else:
        # Login por username
        user = db.query(models_sql.User).filter(models_sql.User.username == request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado ou incorreto")
    if not Hash.verify(request.password, user.senha):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado ou incorreto")

    access_token_expires = timedelta(minutes=JWT_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWT_token.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}