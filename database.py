from psycopg import connect
import os
from dotenv import load_dotenv

load_dotenv()

host=os.getenv("db_host")
port=int(os.getenv("db_port"))
dbname=os.getenv("db_name")
user=os.getenv("db_user")
password=os.getenv("db_password")

connection=connect(host=host,port=port,dbname=dbname,user=user,password=password)

