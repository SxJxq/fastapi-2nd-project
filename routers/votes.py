from fastapi import status, HTTPException, Depends, APIRouter
import schemas, oauth2, modles
from database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_create(vote: schemas.Vote,current_user:int=Depends(oauth2.get_current_user) ,db:Session=Depends(get_db)): 

    voted_post=db.query(modles.Post).filter(modles.Post.id == modles.Vote.post_id)
    if not voted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")
    
    voted=db.query(modles.Vote).filter(modles.Vote.post_id==vote.post_id, modles.Vote.user_id==current_user.id).first()

    if vote.dir==1:
        if voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id} already voted on this post")
        
        new_vote=modles.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        
        return{"msg":"voted"}
    
    else:
        if not voted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesnt exist")
        
        voted.delete(Synchronize_session=False)
        db.commit()
        return {"msg":"unvoted"}
    
    
    