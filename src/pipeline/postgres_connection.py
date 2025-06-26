from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

def get_postgres_connection():
    """
    Establish a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None
    
def close_postgres_connection(conn):
    """
    Close the PostgreSQL database connection.
    """
    if conn:
        try:
            conn.close()
            print("PostgreSQL connection closed.")
        except Exception as e:
            print(f"Error closing PostgreSQL connection: {e}")
    else:
        print("No connection to close.")

def get_motor_timeseries(conn, motor_name: str) -> pd.DataFrame:
    with conn.cursor() as cur:
        # 1. Find tag IDs
        tag_types = ['power', 'rpm', 'temperature', 'vibration']
        tag_ids = {}
        for tag_type in tag_types:
            cur.execute(
                """
                SELECT id FROM sqlth_te 
                WHERE tagpath ILIKE %s 
                ORDER BY id LIMIT 1
                """,
                (f"%{motor_name}%{tag_type}%",)
            )
            result = cur.fetchone()
            if not result:
                raise ValueError(f"Tag ID for '{tag_type}' not found for motor '{motor_name}'")
            tag_ids[tag_type] = result[0]

        # 2. Discover available partitioned tables
        cur.execute("""
            SELECT tablename
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public' AND tablename LIKE 'sqlt_data_1_%'
        """)
        tables = [row[0] for row in cur.fetchall()]
        if not tables:
            raise RuntimeError("No sqlt_data_1_* tables found in the database.")

    # 3. Build and execute queries for each partition
    dfs = []
    for table in tables:
        query = f"""
        SELECT
            to_timestamp(p.t_stamp / 1000) AT TIME ZONE 'UTC' AS timestamp,
            false AS is_anomaly,
            'off' AS state,
            'Normal' AS label,
            p.floatvalue AS power,
            r.floatvalue AS rpm,
            t.floatvalue AS temperature,
            v.floatvalue AS vibration
        FROM public.{table} p
        JOIN public.{table} r ON p.t_stamp = r.t_stamp
        JOIN public.{table} t ON p.t_stamp = t.t_stamp
        JOIN public.{table} v ON p.t_stamp = v.t_stamp
        WHERE p.tagid = {tag_ids['power']}
          AND r.tagid = {tag_ids['rpm']}
          AND t.tagid = {tag_ids['temperature']}
          AND v.tagid = {tag_ids['vibration']}
        """
        try:
            df = pd.read_sql_query(query, conn)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            print(f"Warning: Skipping table {table} due to error: {e}")

    if not dfs:
        raise RuntimeError("No data returned from any partition.")

    # 4. Combine and return
    return pd.concat(dfs).sort_values("timestamp").reset_index(drop=True)


def get_all_motor_names(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT tagpath FROM sqlth_te WHERE tagpath ILIKE '%motor%'
        """)
        rows = cur.fetchall()

    import re
    motor_names = set()
    for (tagpath,) in rows:
        match = re.search(r'motor[\w]+', tagpath)
        if match:
            motor_names.add(match.group(0))
    return sorted(motor_names)


def save_anomaly_results(conn, df, table_name="anomaly_results"):
    """Insert rows from `df` into `table_name` using the existing connection."""
    cols = list(df.columns)
    values = [tuple(x) for x in df.to_numpy()]
    with conn.cursor() as cur:
        execute_values(
            cur,
            f"INSERT INTO {table_name} ({','.join(cols)}) VALUES %s",
            values
        )
    conn.commit()



if __name__ == "__main__":
    conn = get_postgres_connection()
    if conn:
        try:
            all_motor =  get_all_motor_names(conn)
            print("Available motors:", all_motor)
            motor_name="/motor6/"
            df = get_motor_timeseries(conn, motor_name)
            print(df.head())
        finally:
            close_postgres_connection(conn)



