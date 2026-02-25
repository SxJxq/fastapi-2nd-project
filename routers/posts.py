import modles, schemas,utils, oauth2
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Optional

router= APIRouter(
    prefix="/posts",
    tags=['Post']
)


#GET ALL POSTS
@router.get("/",response_model=List[schemas.PostOut])
def get_users(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user), limit=10, skip=0, search=Optional[str]=""):
    posts=db.query(modles.Post).filter(modles.Post.contains(search).limit(limit).offset(skip)).all()
    return posts

#GET ONE POST BY ID
@router.get("/{id}",response_model=List[schemas.PostOut])
def get_users(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user), limit=10, skip=0, search=Optional[str]=""):
    post=db.query(modles.Post).filter(modles.Post.id == id).first()
    return post

#CREATE POST
@router.post("/post", response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
def post_create( post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    new_post=modles.Post(owner_id=current_user.id, **post.model_dump)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#UPDATE POST
@router.put("/{id}",response_model=schemas.PostOut)
def post_update(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user), ):
    post=db.query(modles.Post).filter(modles.Post.id == id)

    if post in None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user does not own the post")
    
    post.update(updated_post.model_dump, synchronize_session=False)
    db.commit(post)

    return post

#DELETE POST
@router.put("/{id}",response_model=schemas.PostOut, status_code=status.HTTP_204_NO_CONTENT)
def post_update(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user), ):
    post=db.query(modles.Post).filter(modles.Post.id == id)

    if post in None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user does not own the post")
    
    post.delete(synchronize_session=False)
    db.commit(post)


