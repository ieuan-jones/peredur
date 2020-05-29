import psycopg2

schema_history = [
    {
        'version': 1,
        'scripts': [
            'schema.sql',
            'activity.sql',
            'activity_record.sql',
            'user.sql'
        ]
    }
]

def connect():
    '''Connect to postgres instance running in local docker container.
    Return: database connection, schema version of database'''

    # Only local development variables, please no one get too excited!
    conn = psycopg2.connect('host=localhost dbname=postgres user=postgres password=docker')

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT version FROM schema;')
        records = cursor.fetchall()

        return records[0][0]
    except psycopg2.errors.UndefinedTable:
        # The database hasn't been set up for the first time yet
        conn.rollback()
        initialise(conn)
        return 1
    finally:
        cursor.close()
        conn.close()
    
    return version

def initialise(conn):
    # Now set up the database. We'll do this by applying every version
    # sequentially for the history of the project
    cursor = conn.cursor()
    for schema in schema_history:
        for script in schema['scripts']:
            # Read the SQL file we want to apply to our database
            with open(f'src/sql/schemas/{script}', 'r') as schema_file:    
                sql = schema_file.read()
            # And execute it
            cursor.execute(sql)
        # Insert the appropriate schema version into the database
        cursor.execute('INSERT INTO schema (SELECT %s AS version);', (schema['version'],))
    conn.commit()


