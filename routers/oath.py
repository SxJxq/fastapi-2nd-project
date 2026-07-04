from fastapi import APIRouter, Depends, HTTPException, status
import schemas, modles, oauth2
from database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils import verify

router=APIRouter(
    tags=['login']
)

@router.post('/login', response_model=schemas.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(modles.User).filter(modles.User.email == user_credentials.username).first()

    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Username and Password required")
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token=oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token, "token_type":"bearer"}