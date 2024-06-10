import os
from dotenv import load_dotenv
from Libraries import *
load_dotenv()

def uat_connection():
     logging.info("Connecting to UAT Database...")
     username = os.getenv('username_uat')
     password = os.getenv('password_uat')
     host = os.getenv('host_uat')
     port = os.getenv('port_uat')
     database = os.getenv('database_uat')
     Database_url_uat = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
               username,password,host,port,database
          )
     return Database_url_uat