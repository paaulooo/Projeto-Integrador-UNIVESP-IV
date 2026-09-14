from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


from app.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def sync_tables(model, engine):
    inspector = inspect(engine)
    table_name = model.__tablename__
    columns_db = inspector.get_columns(table_name)
    columns_model = [c.name for c in model.__table__.columns]

    columns_diff = set(columns_model) - {c["name"] for c in columns_db}

    with engine.connect() as conn:
        for column in columns_diff:
            columns_to_add = model.__table__.columns[column]
            sql_type = columns_to_add.type.compile(engine.dialect)
            conn.execute(text(
                f"ALTER TABLE {table_name} ADD COLUMN {column} {sql_type}"
            ))
            conn.commit()

            

        
            

    
    