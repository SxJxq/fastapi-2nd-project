#CREATING A USER
import modles, schemas,utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router= APIRouter(
    prefix="/users",
    tags=['Users']
)

#CREATE USER
@router.post("/cr",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def creat_user(user:schemas.CreateUser, db: Session=Depends(get_db)):

    pre_email=db.query(modles.User).filter(modles.User.email == user.email).first()

    if pre_email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User with such email already exists")

    hashed_pass=utils.hash(user.password)
    user.password=hashed_pass

    new_user=modles.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#RETREIVE USER IN ID
@router.get("/{id}", response_model=schemas.UserOut)
def retrieve_user(id:int, db: Session=Depends(get_db)):
    ret_user=db.query(modles.User).filter(modles.User.id == id).first()

    if not ret_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")

    return ret_user

#GET ALL USERS
@router.get("/", response_model=List[schemas.UserOut])
def all_users(db: Session=Depends(get_db)):
    users=db.query(modles.User).all()
    return users

#DELETE A USER
@router.post("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, user:schemas.CreateUser, db:Session=Depends(get_db)):
    deleted_user=db.query(modles.User).filter(modles.User.id == id).first()

    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    
    db.delete(deleted_user)
    db.commit()