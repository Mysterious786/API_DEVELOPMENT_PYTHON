from .. import models, schemas
from fastapi import  status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from typing import  List
from ..database import  SessionLocal

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()







@router.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    #print(posts)
    posts = db.query(models.Post).all()
    return posts

# titlw,str, content str
# bool published post
# create ---->  post status code 201
@router.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO post (title,content,is_published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.is_published))
    #conn.commit()
    #new_post = cursor.fetchone()
    #new_posts = models.Post(title=post.title,content=post.content,is_published=post.is_published)
    new_posts = models.Post(**post.model_dump())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return post


@router.get("/posts/{id}") # id field represent path parameter
def get_posts(id: int,db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * from post WHERE  eid=%s """,(str(id),))
    #post = cursor.fetchone()
    #print(post)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"post_detail":post}

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
    
        
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    #find the index in the array
    #my_post.pop(ind)
   # cursor.execute("""DELETE from post where eid=%s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
def update_post(id:int,updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    #print(post)
    #cursor.execute("""UPDATE post SET title = %s, content=%s, is_published=%s WHERE eid = %s returning *""",(post.title,post.content,post.is_published,str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()