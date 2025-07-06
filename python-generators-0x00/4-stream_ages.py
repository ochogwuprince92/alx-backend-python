import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one from the DB"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='devuser',
            password='Devpass123!',
            database='ALX_prodev'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # only 1 loop here
            yield age

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def average_user_age():
    """Uses the generator to compute average age without loading all data"""
    total = 0
    count = 0

    for age in stream_user_ages():  # 2nd loop
        total += float(age)
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")
