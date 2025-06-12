import os
from sqlmodel import create_engine
from dotenv import load_dotenv

load_dotenv()

sqlite_url = f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_ADDR']}/learndb"

engine = create_engine(sqlite_url)
