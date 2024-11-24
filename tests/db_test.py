from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def test_db_connection():
    DATABASE_URL = "postgresql://test_user:testpass123@localhost:5432/test_db"
    
    engine = create_engine(DATABASE_URL)
    
    if not database_exists(engine.url):
        create_database(engine.url)
    
    try:
        connection = engine.connect()
        print("Successfully connected to the database!")
        connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    test_db_connection() 