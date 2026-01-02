#!/usr/bin/env python3
"""
Import MySQL dump files to PostgreSQL for fightsToday
"""

import psycopg2
import re
import sys

POSTGRES_CONFIG = {
    'host': '192.168.1.23',
    'user': 'postgres',
    'password': 'korn5676',
    'dbname': 'fights_today'
}

def mysql_to_postgres_value(val):
    """Convert MySQL value to PostgreSQL"""
    if val == 'NULL':
        return 'NULL'
    return val

def parse_insert_statement(line):
    """Parse MySQL INSERT statement and convert to PostgreSQL format"""
    match = re.match(r"INSERT INTO `([^`]+)` VALUES\s*(.+);", line)
    if not match:
        return None, None

    table_name = match.group(1)
    values_str = match.group(2)
    return table_name, values_str

def process_dump_file(filepath, pg_conn):
    """Process a MySQL dump file and import to PostgreSQL"""
    print(f"Processing {filepath}...")

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        current_table = None
        insert_count = 0

        for line_num, line in enumerate(f, 1):
            line = line.strip()

            if line.startswith('INSERT INTO'):
                table_name, values_str = parse_insert_statement(line)
                if table_name and values_str:
                    if table_name != current_table:
                        current_table = table_name
                        print(f"  Importing into table: {table_name}")

                    pg_sql = f'INSERT INTO "{table_name}" VALUES {values_str};'
                    pg_sql = pg_sql.replace('`', '"')
                    pg_sql = pg_sql.replace('\\\'', "''")
                    pg_sql = re.sub(r'\\([^\\])', r'\1', pg_sql)

                    try:
                        with pg_conn.cursor() as cur:
                            cur.execute(pg_sql)
                        pg_conn.commit()
                        insert_count += 1
                        if insert_count % 100 == 0:
                            print(f"    Processed {insert_count} inserts...", end='\r')
                    except Exception as e:
                        pg_conn.rollback()
                        print(f"\n    Error at line {line_num}: {e}")
                        print(f"    SQL preview: {pg_sql[:200]}...")

        print(f"  Completed: {insert_count} inserts")

def main():
    print("=" * 60)
    print("MySQL Dump to PostgreSQL Import")
    print("=" * 60)

    print("\nConnecting to PostgreSQL...")
    try:
        pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
        print(f"  Connected to {POSTGRES_CONFIG['host']}/{POSTGRES_CONFIG['dbname']}")
    except Exception as e:
        print(f"  ERROR: {e}")
        sys.exit(1)

    dump_files = [
        '/export/main_tables.sql',
        '/export/odds.sql',
        '/export/odds_history.sql'
    ]

    for filepath in dump_files:
        try:
            process_dump_file(filepath, pg_conn)
        except FileNotFoundError:
            print(f"  File not found: {filepath}")

    pg_conn.close()
    print("\nDone!")

if __name__ == "__main__":
    main()
