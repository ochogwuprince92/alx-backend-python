import mysql.connector

def stream_users_in_batches(batch_size):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='devuser',
            password='Devpass123!',
            database='ALX_prodev'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            return rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
