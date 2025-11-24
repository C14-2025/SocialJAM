import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")

# Permitir fallback apenas em modo de testes
if not SECRET_KEY:
    if os.getenv("TESTING", "").lower() == "true":
        SECRET_KEY = "chave_secreta_para_testes_hehe"
    else:
        raise ValueError("SECRET_KEY não está definida! Configure a variável de ambiente SECRET_KEY no arquivo .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt