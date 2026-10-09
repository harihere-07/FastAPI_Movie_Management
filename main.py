from fastapi import FastAPI,Depends
from database import connection
from pydantic import BaseModel
from auth import auth,security,algorithm,secret_key,jwt
import bcrypt
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv

load_dotenv()

app=FastAPI()


class Register(BaseModel):
    username:str
    password:str

@app.post("/create_account")

def create_acc(regist:Register):

    cursor=connection.cursor()
    salt=bcrypt.gensalt()
    hashed_pass=bcrypt.hashpw(
        regist.password.encode(),
        salt
    ).decode()

    cursor.execute('''Insert into "user_table"("username","hashed_password")
    values(%s,%s)''',(regist.username,hashed_pass))

    connection.commit()
    return {"Message":"Inserted successfully"}

class Login(BaseModel):
    username:str
    password:str

@app.post("/login")
def login_page(req=Depends(OAuth2PasswordRequestForm)):


    cursor=connection.cursor()
    cursor.execute('''select * from "user_table"
    where "username"=%s''',(req.username,))
    fetch=cursor.fetchone()
    user=fetch[2]
    result=bcrypt.checkpw(req.password.encode(),user.encode())
    if result==True:
        token=auth(req.username)
        return {
            "username":req.username,
            "access_token":token,
            "token_type":"bearer"
        }
    else:
        return {"message":"login failed invalid user"}



class Movies(BaseModel):
    title:str
    genre:str
    year:int
    rating:float

@app.post("/movies")
def create_movies(movie:Movies,tok=Depends(security)):
    token=tok
    decoded=jwt.decode(token,secret_key,algorithm) 
    username=decoded["username"]
    movie.title
    movie.genre
    movie.year
    movie.rating

    cursor=connection.cursor()
    cursor.execute('''Insert into movies_table("title","genre","year","rating")
    values(%s,%s,%s,%s)''',(movie.title,movie.genre,movie.year,movie.rating))
    connection.commit()
    cursor.execute('''select * from movies_table''')
    fetch=cursor.fetchall()
    return fetch

@app.put("/upd_movies/{movie_id}")
def update_movies(movie:Movies,movie_id:int,tok=Depends(security)):
    token=tok.credentials
    decoded=jwt.decode(token,secret_key,algorithm) 
    username=decoded["username"]
    movie.title
    movie.genre
    movie.year
    movie.rating

    cursor=connection.cursor()
    
    cursor.execute('''update movies_table set "title"=%s,
    "genre"=%s,"year"=%s,"rating"=%s where "movie_id"=%s''',
    (movie.title,movie.genre,movie.year,movie.rating,movie_id))

    connection.commit()
    cursor.execute('''select * from movies_table''')
    fetch=cursor.fetchall()
    return fetch

@app.get("/get_movies/{movie_id}")
def read_movies(movie_id:int,tok=Depends(security)):
    token=tok.credentials
    decoded=jwt.decode(token,secret_key,algorithm) 
    username=decoded["username"]

    cursor=connection.cursor()
    cursor.execute('''select * from movies_table
    where "movie_id"=%s''',(movie_id,))
    fetch=cursor.fetchone()
    return fetch

@app.get("/get_all_movies")
def read_all_movies(tok=Depends(security)):
    token=tok.credentials
    decoded=jwt.decode(token,secret_key,algorithm) 
    username=decoded["username"]
    cursor=connection.cursor()
    cursor.execute('''select * from movies_table''')
    fetch=cursor.fetchall()
    return fetch

@app.delete("/delete_movies")
def delete_movie(movie_id:int,tok=Depends(security)):
    token=tok.credentials
    decoded=jwt.decode(token,secret_key,algorithm) 
    username=decoded["username"]
    
    cursor=connection.cursor()
    cursor.execute('''delete from movies_table 
    where "movie_id"=%s''',(movie_id,))
    connection.commit()
    cursor.execute('''select * from movies_table''')
    fetch=cursor.fetchall()
    print("Record Deleted successfully")
    return fetch