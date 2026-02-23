from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import settings
import schemas



oath2_scheme=OAuth2PasswordBearer('login')

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes

def create_access_token(data:dict):
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode=data.copy()
    to_encode.update({"exp":expire})

    encoded_data=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_data

def verify_access_token(token:str, credentials_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)

        userid:str=payload.get(token)

        if not userid:
            raise credentials_exception
    
        token_data=schemas.TokenData(id=(str)id)

    except JWTError:
        raise credentials_exception
    
    return token_data



