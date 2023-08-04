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
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host="localhost",
                            database="ad-dm", 
                            user="postgres", 
                            password="windows8",
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Databaase connection was successfull")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"content":"This is my first post", "title":"My first post", "id" : 1},
            {"content" : "This is my second post", "title" : "My second post", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/query1")
def get_query1():
    cursor.execute("""SELECT e.emp_no, e.last_name, e.first_name, e.sex, s.salary
                    FROM employees e, salaries s
                    WHERE e.emp_no = s.emp_no LIMIT 20""")
    rows = cursor.fetchall()
    return {"data": rows}

@app.get("/query2")
def get_query2():
    cursor.execute("""SELECT first_name, last_name, hire_date
                    FROM employees
                    WHERE EXTRACT(YEAR FROM hire_date) = 1986
                    LIMIT 20""")
    rows = cursor.fetchall()
    return {"data": rows}

@app.get("/query3")
def get_query3():
    cursor.execute("""SELECT m.dept_no, d.dept_name, m.emp_no, e.last_name, e.first_name
                    FROM dept_manager m, employees e, departments d
                    WHERE m.dept_no = d.dept_no and e.emp_no = m.emp_no""")
    rows = cursor.fetchall()
    return {"data": rows}

@app.get("/query4")
def get_query4():
    cursor.execute("""SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
                    FROM employees e, departments d, dept_emp dp
                    WHERE e.emp_no = dp.emp_no and d.dept_no = dp.dept_no
                    LIMIT 20""")
    rows = cursor.fetchall()
    return {"data": rows}

@app.get("/query5")
def get_query5():
    cursor.execute("""SELECT first_name, last_name, sex
                    FROM employees
                    WHERE first_name = 'Hercules' and last_name LIKE 'B%' """)
    rows = cursor.fetchall()
    return {"data": rows}

@app.get("/query6")
def get_query6():
    cursor.execute("""SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
                    FROM employees e
                    INNER JOIN dept_emp dp ON e.emp_no = dp.emp_no
                    INNER JOIN departments d ON dp.dept_no = d.dept_no
                    WHERE d.dept_name = 'Sales'
                    LIMIT 20""")
    rows = cursor.fetchall()
    return {"data": rows}

@app.get("/query7")
def get_query7():
    cursor.execute("""SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
                    FROM employees e
                    INNER JOIN dept_emp dp ON e.emp_no = dp.emp_no
                    INNER JOIN departments d ON dp.dept_no = d.dept_no
                    WHERE d.dept_name = 'Sales' OR d.dept_name = 'Development'
                    LIMIT 20""")
    rows = cursor.fetchall()
    return {"data": rows}

@app.get("/query8")
def get_query8():
    cursor.execute("""SELECT last_name, COUNT(*) as num_emp
                    FROM employees
                    GROUP BY last_name
                    ORDER BY num_emp DESC""")
    rows = cursor.fetchall()
    return {"data": rows}

@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                (new_post.title, new_post.content, new_post.published))
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

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {"data": updated_post}