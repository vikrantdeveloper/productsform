"""
Created on March 16, 2025

@author: Vikrant
"""
import pymysql
import aws_credentials as rds

def get_db_connection():
    """Establish and return a database connection."""
    try:
        return pymysql.connect(
            host=rds.host,
            port=rds.port,
            user=rds.user,
            password=rds.password,
            db=rds.db
        )
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_table_if_not_exists():
    """Create the Details table if it does not exist."""
    conn = get_db_connection()
    if conn is None:
        return
    
    try:
        with conn.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Details (
                id VARCHAR(200) PRIMARY KEY,  
                description VARCHAR(200),  
                price VARCHAR(200)
            );
            """
            cursor.execute(create_table_query)
            conn.commit()
    except pymysql.MySQLError as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

# Function to Add Product
def add_product(id, description, price):
    """Insert a new product into the Details table."""
    conn = get_db_connection()
    if conn is None:
        return
    
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO Details (id, description, price) VALUES (%s, %s, %s)"
            cur.execute(sql, (id, description, price))
            conn.commit()
    except pymysql.MySQLError as e:
        print(f"Error inserting product: {e}")
    finally:
        conn.close()

# Function to List Products
def list_product():
    """Retrieve all products from the Details table."""
    conn = get_db_connection()
    if conn is None:
        return []
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Details")
            details = cur.fetchall()
            return details
    except pymysql.MySQLError as e:
        print(f"Error fetching products: {e}")
        return []
    finally:
        conn.close()

# Function to delete all the products 
def delete_all_products():
    """Delete all records from the Details table."""
    conn = get_db_connection()
    if conn is None:
        return
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Details;")
            conn.commit()
    except pymysql.MySQLError as e:
        print(f"Error deleting products: {e}")
    finally:
        conn.close()

