from fastapi import APIRouter, Depends
from app import schemas, database, models_sql
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
async def login(request: schemas.Login, db:Session = Depends(database.get_db)):
    # Lógica de login básica (ainda não implementada completamente)
    if "@" in request.username_email:
        # Login por email
        user = db.query(models_sql.User).filter(models_sql.User.email == request.username_email).first()
    else:
        # Login por username
        user = db.query(models_sql.User).filter(models_sql.User.username == request.username_email).first()
    
    return {"message": "Login endpoint", "user_found": user is not None}