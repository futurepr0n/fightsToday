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

        # Handle ON DUPLICATE KEY UPDATE - convert to PostgreSQL ON CONFLICT
        if 'ON DUPLICATE KEY UPDATE' in pg_query.upper():
            pg_query = convert_mysql_upsert_to_postgres(pg_query)

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
        print(f"Query was: {pg_query[:200]}...")
        if pg_conn:
            pg_conn.rollback()
            pg_conn.close()
        return False


def convert_mysql_upsert_to_postgres(query):
    """Convert MySQL ON DUPLICATE KEY UPDATE to PostgreSQL ON CONFLICT"""
    import re

    # Split on ON DUPLICATE KEY UPDATE
    parts = re.split(r'ON\s+DUPLICATE\s+KEY\s+UPDATE', query, flags=re.IGNORECASE)
    if len(parts) != 2:
        return query

    insert_part = parts[0].strip()
    update_part = parts[1].strip()

    # Extract the table name from INSERT INTO table_name
    table_match = re.search(r'INSERT\s+INTO\s+["\']?(\w+)["\']?', insert_part, re.IGNORECASE)
    if not table_match:
        return insert_part  # Fall back to just the insert

    table_name = table_match.group(1)

    # Map table names to their unique/primary key columns
    table_unique_keys = {
        'wiki_mma_events_poster': 'wiki_event_poster_id',
        'wiki_mma_events': 'wiki_event_id',
        'wiki_mma_fight_cards': 'wiki_fight_id',
        'sd_mma_events': 'sd_event_id',
        'sd_mma_fight_cards': 'id',  # May need adjustment
    }

    unique_key = table_unique_keys.get(table_name)

    if not unique_key:
        # No known unique key, just do the insert and handle conflicts by doing nothing
        return insert_part + " ON CONFLICT DO NOTHING"

    # Convert MySQL VALUES(column) syntax to PostgreSQL EXCLUDED.column syntax
    pg_update_part = re.sub(
        r'VALUES\s*\(\s*(\w+)\s*\)',
        r'EXCLUDED.\1',
        update_part,
        flags=re.IGNORECASE
    )

    # Build PostgreSQL upsert query
    pg_query = f"{insert_part} ON CONFLICT ({unique_key}) DO UPDATE SET {pg_update_part}"

    return pg_query


def truncate_postgres_table(table_name):
    """Truncate a table in PostgreSQL"""
    return execute_on_postgres(f'TRUNCATE TABLE "{table_name}"')


def delete_from_postgres(table_name, where_clause="", params=None):
    """Delete from a PostgreSQL table"""
    query = f'DELETE FROM "{table_name}"'
    if where_clause:
        query += f" WHERE {where_clause}"
    return execute_on_postgres(query, params)
