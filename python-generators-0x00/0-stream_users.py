import mysql.connector

def stream_users():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='devuser',
            password='Devpass123!',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        
        for row in cursor:  # This is a generator under the hood
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
