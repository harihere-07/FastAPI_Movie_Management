from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import timedelta,timezone,datetime
from dotenv import load_dotenv
from fastapi import Depends
import jwt
import os

load_dotenv()
secret_key=os.getenv("secret_key")
algorithm=os.getenv("algorithm")
Access_token_expiry_minutes=int(os.getenv("Access_token_expiry_minutes"))

security=OAuth2PasswordBearer(
    tokenUrl="/login"
)

def auth(username):
    expire=datetime.now(timezone.utc)+timedelta(minutes=Access_token_expiry_minutes)
    payload={
        "username":username,
        "exp":expire
    }


    token=jwt.encode(payload,secret_key,algorithm)
    return token