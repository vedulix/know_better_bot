import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def init_test_db():
    # Загрузка переменных окружения из .env.test
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env.test'
    load_dotenv(env_path)
    
    # Формирование URL для подключения
    DATABASE_URL = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    
    engine = create_engine(DATABASE_URL)
    
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Created database: {os.getenv('POSTGRES_DB')}")
    else:
        print(f"Database already exists: {os.getenv('POSTGRES_DB')}")
    
    try:
        connection = engine.connect()
        print("Successfully connected to the database!")
        connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_test_db() 