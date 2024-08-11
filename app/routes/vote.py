from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
) -> dict:
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, 
        models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:  # Upvote
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Already voted up!!!"
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted"}
    
    elif vote.dir == 0:  # Downvote
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No vote found to delete!!!"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully vote deleted"}

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid vote direction"
        )

