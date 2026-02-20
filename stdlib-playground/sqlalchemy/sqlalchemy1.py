# run with the web_travel venv to have access to sqlalchemy
# postgresql service/server runs with Windows start (remove it later)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DATABASE_URL = 'postgresql+psycopg2://xxx:xxx@localhost:5432/web_travel_dev'

def main():
    engine = create_engine(DATABASE_URL, echo=True)

    if False:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM public.user")) # if not public. -> postgres
            print(result.all())

            # commit as you go
            conn.execute(text("CREATE TABLE IF NOT EXISTS _temp (x int, y int)"))
            conn.execute(
                text("INSERT INTO _temp (x, y) VALUES (:x, :y)"),
                [{'x': 1, 'y': 1}, {'x':2, 'y': 4}] # bound parameters passed as dict or list[dict]
            )
            conn.commit()

        # begin once as a block, auto-commit at the end - preferred
        with engine.begin() as db_conn:
            db_conn.execute(text("DROP TABLE _temp"))

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM public.user"))
        mapps = result.mappings() # read-only dict-like
        print(type(mapps), mapps.__class__.__bases__)


    # ORM-style
    stmt = text("SELECT * FROM user")
    with Session(engine) as session: # the session drops and re-creates connections
        result = session.execute(stmt, {'willbeignored': 55}) # bound param not used
        print(result.all())

    print('--- END ---')

if __name__ == '__main__':
    main()
