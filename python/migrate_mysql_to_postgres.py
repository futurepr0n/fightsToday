#!/usr/bin/env python3
"""
MySQL to PostgreSQL Migration Script for fightsToday
Exports data from MySQL and imports into PostgreSQL
"""

import pymysql
import psycopg2
import sys

# MySQL connection (source)
MYSQL_CONFIG = {
    'host': 'fights.today',
    'port': 3306,
    'user': 'mark5463_ft_test',
    'password': 'fttesting66',
    'database': 'mark5463_ft_prod',
    'charset': 'utf8',
    'connect_timeout': 30,
    'read_timeout': 300,
    'write_timeout': 300
}

# PostgreSQL connection (destination)
POSTGRES_CONFIG = {
    'host': '192.168.1.23',
    'user': 'postgres',
    'password': 'korn5676',
    'dbname': 'fights_today'
}

def get_mysql_tables(mysql_cur):
    """Get list of all tables in MySQL database"""
    mysql_cur.execute("SHOW TABLES")
    return [table[0] for table in mysql_cur.fetchall()]

def get_mysql_table_schema(mysql_cur, table_name):
    """Get column info for a MySQL table"""
    mysql_cur.execute(f"DESCRIBE `{table_name}`")
    return mysql_cur.fetchall()

def mysql_type_to_postgres(mysql_type):
    """Convert MySQL data type to PostgreSQL equivalent"""
    mysql_type = mysql_type.lower()

    if 'int' in mysql_type:
        return 'INTEGER'
    elif 'varchar' in mysql_type:
        # Extract length: varchar(500) -> VARCHAR(500)
        return mysql_type.upper().replace('VARCHAR', 'VARCHAR')
    elif 'char(' in mysql_type:
        return mysql_type.upper()
    elif 'text' in mysql_type:
        return 'TEXT'
    elif 'boolean' in mysql_type or 'tinyint(1)' in mysql_type:
        return 'BOOLEAN'
    elif 'datetime' in mysql_type:
        return 'TIMESTAMP'
    elif 'date' in mysql_type:
        return 'DATE'
    elif 'decimal' in mysql_type or 'float' in mysql_type or 'double' in mysql_type:
        return 'NUMERIC'
    else:
        return 'TEXT'

def generate_postgres_create_table(mysql_cur, table_name):
    """Generate PostgreSQL CREATE TABLE statement from MySQL schema"""
    schema = get_mysql_table_schema(mysql_cur, table_name)

    columns = []
    for col in schema:
        col_name = col[0]
        col_type = mysql_type_to_postgres(col[1])
        nullable = "NULL" if col[2] == "YES" else "NOT NULL"
        columns.append(f'    "{col_name}" {col_type} {nullable}')

    return f'CREATE TABLE IF NOT EXISTS "{table_name}" (\n' + ',\n'.join(columns) + '\n);'

def get_table_columns(mysql_cur, table_name):
    """Get column names for a table"""
    mysql_cur.execute(f"SELECT * FROM `{table_name}` LIMIT 1")
    columns = [desc[0] for desc in mysql_cur.description]
    mysql_cur.fetchall()
    return columns

def export_table_data_paginated(mysql_conn, table_name, batch_size=5000):
    """Export data using LIMIT/OFFSET pagination for large tables"""
    cur = mysql_conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM `{table_name}`")
    total_rows = cur.fetchone()[0]

    columns = get_table_columns(cur, table_name)

    offset = 0
    while offset < total_rows:
        cur.execute(f"SELECT * FROM `{table_name}` LIMIT {batch_size} OFFSET {offset}")
        rows = cur.fetchall()
        if not rows:
            break
        print(f"    Fetched {min(offset + len(rows), total_rows)}/{total_rows} rows...", end='\r')
        yield columns, rows
        offset += batch_size

    print(f"    Fetched {total_rows} rows total    ")
    cur.close()

def import_to_postgres(pg_cur, table_name, columns, rows):
    """Import data into PostgreSQL table"""
    if not rows:
        print(f"  No data to import for {table_name}")
        return 0

    # Create INSERT statement with placeholders
    col_names = ', '.join([f'"{col}"' for col in columns])
    placeholders = ', '.join(['%s'] * len(columns))
    insert_sql = f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})'

    count = 0
    for row in rows:
        # Convert any None values and handle encoding
        cleaned_row = []
        for val in row:
            if val is None:
                cleaned_row.append(None)
            elif isinstance(val, bytes):
                cleaned_row.append(val.decode('utf-8', errors='replace'))
            else:
                cleaned_row.append(val)

        try:
            pg_cur.execute(insert_sql, tuple(cleaned_row))
            count += 1
        except Exception as e:
            print(f"  Error inserting row: {e}")
            print(f"  Row data: {cleaned_row[:3]}...")  # Print first 3 cols for debug

    return count

def main():
    print("=" * 60)
    print("MySQL to PostgreSQL Migration for fightsToday")
    print("=" * 60)

    # Step 1: Connect to MySQL
    print("\n[1] Connecting to MySQL...")
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cur = mysql_conn.cursor()
        print(f"    Connected to MySQL: {MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}")
    except Exception as e:
        print(f"    ERROR connecting to MySQL: {e}")
        sys.exit(1)

    # Step 2: Get list of tables
    print("\n[2] Getting table list from MySQL...")
    tables = get_mysql_tables(mysql_cur)
    print(f"    Found {len(tables)} tables: {', '.join(tables)}")

    # Step 3: Connect to PostgreSQL
    print("\n[3] Connecting to PostgreSQL...")
    try:
        # First connect without database to create it if needed
        pg_conn_init = psycopg2.connect(
            host=POSTGRES_CONFIG['host'],
            user=POSTGRES_CONFIG['user'],
            password=POSTGRES_CONFIG['password'],
            dbname='postgres'
        )
        pg_conn_init.autocommit = True
        pg_cur_init = pg_conn_init.cursor()

        # Create database if not exists
        pg_cur_init.execute("SELECT 1 FROM pg_database WHERE datname = %s", (POSTGRES_CONFIG['dbname'],))
        if not pg_cur_init.fetchone():
            print(f"    Creating database '{POSTGRES_CONFIG['dbname']}'...")
            pg_cur_init.execute(f"CREATE DATABASE {POSTGRES_CONFIG['dbname']}")
        else:
            print(f"    Database '{POSTGRES_CONFIG['dbname']}' already exists")

        pg_cur_init.close()
        pg_conn_init.close()

        # Now connect to the actual database
        pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
        pg_conn.autocommit = True
        pg_cur = pg_conn.cursor()
        print(f"    Connected to PostgreSQL: {POSTGRES_CONFIG['host']}/{POSTGRES_CONFIG['dbname']}")
    except Exception as e:
        print(f"    ERROR connecting to PostgreSQL: {e}")
        mysql_conn.close()
        sys.exit(1)

    # Step 4: Create tables in PostgreSQL
    print("\n[4] Creating tables in PostgreSQL...")
    for table in tables:
        create_sql = generate_postgres_create_table(mysql_cur, table)
        print(f"\n    Creating table: {table}")
        print(f"    {'-' * 40}")
        try:
            # Drop existing table first (for clean migration)
            pg_cur.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
            pg_cur.execute(create_sql)
            print(f"    ✓ Table '{table}' created")
        except Exception as e:
            print(f"    ✗ Error creating table '{table}': {e}")

    # Step 5: Export and import data
    print("\n[5] Migrating data...")
    total_rows = 0
    for table in tables:
        print(f"\n    Migrating table: {table}")
        table_count = 0
        for columns, rows in export_table_data_paginated(mysql_conn, table, batch_size=5000):
            if rows:
                count = import_to_postgres(pg_cur, table, columns, rows)
                table_count += count
        total_rows += table_count
        print(f"    ✓ Imported {table_count} rows")

    # Step 6: Summary
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print(f"Tables migrated: {len(tables)}")
    print(f"Total rows imported: {total_rows}")
    print("\nTables created:")
    for table in tables:
        pg_cur.execute(f'SELECT COUNT(*) FROM "{table}"')
        count = pg_cur.fetchone()[0]
        print(f"  - {table}: {count} rows")

    # Cleanup
    mysql_cur.close()
    mysql_conn.close()
    pg_cur.close()
    pg_conn.close()

    print("\nDone!")

if __name__ == "__main__":
    main()
