from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    company_name: str
    required_skills: str
    published_date: str
    more_info: str

while True:
    try:
        conn = psycopg2.connect(host="localhost",
                            database="web_scraping", 
                            user="postgres", 
                            password="windows8",
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM job_list""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute("""INSERT INTO job_list 
                   (company_name, required_skills, published_date, more_info) 
                   VALUES (%s, %s, %s, %s) RETURNING *""",
                (new_post.company_name, new_post.required_skills, new_post.published_date, new_post.more_info))
    post = cursor.fetchone()
    conn.commit()
    return {"data" : post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", [id])
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"post with id {id} was not found"}
    return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", [id])
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)