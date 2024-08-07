from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


my_posts = [{
    "title": "Title of post1",
    "content": "Content of post1",
    "id" : 1
},
{
    "title" : "Favourite foods",
    "content" : "I like pizza",
    "id": 2
}



]
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        

class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='S@q12345',cursor_factory=RealDictCursor) # host,databse,user,password
        cursor = conn.cursor()
        print("Database connected successfully!!!")
        break
    except Exception as error:
        print("Connection failed!!!")
        print(f"Error was : {error}")
        time.sleep(2)

@app.get("/")
async def root():
    return {"message":"Hello How are you, any problem"}
# : dict = Body(...) payload['title] pydantic for schema

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    print(posts)
    return {"data":my_posts}

# titlw,str, content str
# bool published post
# create ---->  post status code 201
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO post (title,content,is_published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.is_published))
    conn.commit()
    new_post = cursor.fetchone()
    return {"data":new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}


@app.get("/posts/{id}") # id field represent path parameter
def get_posts(id: int):
    cursor.execute("""SELECT * from post WHERE  eid=%s """,(str(id),))
    post = cursor.fetchone()
    print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"post_detail":post}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    
        
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #find the index in the array
    #my_post.pop(ind)
    cursor.execute("""DELETE from post where eid=%s returning *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post: Post):
    #print(post)
    cursor.execute("""UPDATE post SET title = %s, content=%s, is_published=%s WHERE eid = %s returning *""",(post.title,post.content,post.is_published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'data':updated_post}