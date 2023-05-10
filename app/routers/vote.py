import models, schemas, utils, database
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import routers
import sqlalchemy
from typing import List
from sqlalchemy.orm import Session
import utils
import oauth2

router = APIRouter(prefix="/vote", tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post id:{vote.post_id}not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                     models.Vote.user_id == current_user.id)
    if vote_query.first():
        vote.dir = 0

    if (vote.dir == 1):
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "liked a post"}
    else:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "disliked a post"}
        