from fastapi import Depends, HTTPException, status
from . import schemas, database
import os
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(database.get_db)):
    from . import database, models_sql
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    
    # Buscar usuário no banco usando a sessão injetada
    user = db.query(models_sql.User).filter(models_sql.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

    
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data