"""
Simple dual-write module - mirrors MySQL operations to PostgreSQL
"""

import os
import time
import MySQLdb

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("Warning: psycopg2 not installed, PostgreSQL writes will be skipped")

# PostgreSQL configuration
POSTGRES_CONFIG = {
    'host': os.environ.get('PG_HOST', '192.168.1.23'),
    'user': os.environ.get('PG_USER', 'postgres'),
    'password': os.environ.get('PG_PASSWORD', 'korn5676'),
    'dbname': os.environ.get('PG_DATABASE', 'fights_today')
}

POSTGRES_ENABLED = os.environ.get('POSTGRES_ENABLED', 'true').lower() == 'true'


def get_postgres_connection():
    """Get a PostgreSQL connection"""
    if not POSTGRES_AVAILABLE or not POSTGRES_ENABLED:
        return None
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        return conn
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        return None


def execute_on_postgres(query, params=None):
    """Execute a query on PostgreSQL, converting MySQL syntax"""
    if not POSTGRES_AVAILABLE or not POSTGRES_ENABLED:
        return False

    pg_conn = None
    try:
        pg_conn = get_postgres_connection()
        if not pg_conn:
            return False

        cur = pg_conn.cursor()

        # Convert MySQL syntax to PostgreSQL
        pg_query = query.replace('`', '"')

        # Handle ON DUPLICATE KEY UPDATE - convert to simple insert (data will be truncated first anyway)
        if 'ON DUPLICATE KEY UPDATE' in pg_query.upper():
            # Just do the insert part, skip the ON DUPLICATE
            pg_query = pg_query.split('ON DUPLICATE KEY UPDATE')[0].strip()

        if params:
            cur.execute(pg_query, params)
        else:
            cur.execute(pg_query)

        pg_conn.commit()
        cur.close()
        pg_conn.close()
        return True
    except Exception as e:
        print(f"PostgreSQL error: {e}")
        if pg_conn:
            pg_conn.rollback()
            pg_conn.close()
        return False


def truncate_postgres_table(table_name):
    """Truncate a table in PostgreSQL"""
    return execute_on_postgres(f'TRUNCATE TABLE "{table_name}"')


def delete_from_postgres(table_name, where_clause="", params=None):
    """Delete from a PostgreSQL table"""
    query = f'DELETE FROM "{table_name}"'
    if where_clause:
        query += f" WHERE {where_clause}"
    return execute_on_postgres(query, params)
