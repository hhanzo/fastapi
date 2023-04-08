from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional     
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database='fastapi', 
                            user='postgres',password = 'qwerty1234',cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to a database failed!")
        print("Error:",error)
        time.sleep(2)


my_posts = [{"title":"title1","content":"content1","id":1}
            ,{"title":"title2","content":"content2","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(posts:Post):
    post_dict = posts.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/{id}")
def get_post(id:int, response:Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id :{id} was not found"            )
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #find the index in the array that has required ID
    #my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
            , detail = f"post with id {id} doesn't exist!")
    my_posts.pop(index)
    return  Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int,post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {'message':"update_post"}