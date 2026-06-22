from sqlalchemy import create_engine, text

engine = create_engine("postgresql://dvt@localhost:5432/watch_tracker")

create_table_sql = """
DROP TABLE IF EXISTS watches;
CREATE TABLE watches (
    id          SERIAL PRIMARY KEY,
    name        TEXT,
    price       NUMERIC(12, 2),
    brand       VARCHAR(100),
    model       TEXT,
    ref         VARCHAR(100),
    mvmt        VARCHAR(100),
    casem       VARCHAR(100),
    bracem      VARCHAR(100),
    yop         INTEGER,
    cond        TEXT,
    sex         VARCHAR(20),
    size        NUMERIC(5,1),
    condition   VARCHAR(50)
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.commit()
    print("✓ Table created successfully!")