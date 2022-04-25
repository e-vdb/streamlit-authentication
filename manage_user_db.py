from authentication import UsernameDatabase
from dotenv import load_dotenv
import os


load_dotenv()


db = UsernameDatabase(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'),
                      host=os.getenv('HOST'), port=os.getenv('PORT'), database=os.getenv('DATABASE'))
db.connect_to_db()

# Create the table
db.create_table()

# Insert a user
db.insert_user(username="new_user", password="password", app_access="demo")
