from dotenv import load_dotenv
import os
from authentication import UsernameDatabase


load_dotenv()


db = UsernameDatabase(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'), host=os.getenv('HOST'),
                      port=os.getenv('PORT'), database=os.getenv('DATABASE'))
db.connect_to_db()
