from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine(username, password, dbname):
    conn_str = f"postgresql://{username}:{password}@localhost:5432/{dbname}"
    return create_engine(conn_str)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()