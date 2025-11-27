# INITIALIZES THE DATABASE SESSION
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        # 'yield' holds until the entire session is closed (i.e., until session reaches endpoint)
        yield db
    finally:
        db.close()