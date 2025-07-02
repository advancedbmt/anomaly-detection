import psycopg2
import pandas as pd
from core.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def get_postgres_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def get_motor_timeseries(conn, motor_name: str) -> pd.DataFrame:
    tag_types = ['power', 'rpm', 'temperature', 'vibration']
    tag_ids = {}
    with conn.cursor() as cur:
        for tag_type in tag_types:
            cur.execute("SELECT id FROM sqlth_te WHERE tagpath ILIKE %s ORDER BY id LIMIT 1", (f"%{motor_name}%{tag_type}%",))
            result = cur.fetchone()
            if not result:
                raise ValueError(f"Tag ID for {tag_type} not found")
            tag_ids[tag_type] = result[0]

        cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE tablename LIKE 'sqlt_data_1_%'")
        tables = [row[0] for row in cur.fetchall()]

    dfs = []
    for table in tables:
        query = f"""
            SELECT to_timestamp(p.t_stamp / 1000) AT TIME ZONE 'UTC' AS timestamp,
                   p.floatvalue AS power, r.floatvalue AS rpm,
                   t.floatvalue AS temperature, v.floatvalue AS vibration,
                   'off' AS state, false AS is_anomaly, 'Normal' AS label
            FROM {table} p
            JOIN {table} r ON p.t_stamp = r.t_stamp
            JOIN {table} t ON p.t_stamp = t.t_stamp
            JOIN {table} v ON p.t_stamp = v.t_stamp
            WHERE p.tagid = {tag_ids['power']}
              AND r.tagid = {tag_ids['rpm']}
              AND t.tagid = {tag_ids['temperature']}
              AND v.tagid = {tag_ids['vibration']}
        """
        try:
            df = pd.read_sql_query(query, conn)
            if not df.empty:
                dfs.append(df)
        except Exception:
            continue

    if not dfs:
        raise RuntimeError("No data available")

    return pd.concat(dfs).sort_values("timestamp").reset_index(drop=True)

def get_all_motor_names(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT tagpath FROM sqlth_te WHERE tagpath ILIKE '%motor%'")
        rows = cur.fetchall()
    import re
    return sorted({re.search(r'motor[\w]+', row[0]).group(0) for row in rows if re.search(r'motor[\w]+', row[0])})
