from fastapi import FastAPI
from .routes import post,user,auth, vote
# import psycopg2
# from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .config import Settings
models.Base.metadata.create_all(bind=engine)


app = FastAPI()



        


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='S@q12345',cursor_factory=RealDictCursor) # host,databse,user,password
#         cursor = conn.cursor()
#         print("Database connected successfully!!!")
#         break
#     except Exception as error:
#         print("Connection failed!!!")
#         print(f"Error was : {error}")
#         time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
async def root():
    return {"message":"Hello How are you, any problem"}
# : dict = Body(...) payload['title] pydantic for schema

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     #print(posts)
#     return {"data":posts}




