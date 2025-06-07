import psycopg2

def get_connection():
    return psycopg2.connect(
        host = 'localhost',
        database = 'sra_db',
        user = 'sra_user',
        password = 'sra_pass'
    )