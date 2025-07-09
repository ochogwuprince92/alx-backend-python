import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # this will be assigned to the variable in the 'with' statement

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# ✅ Use the context manager to fetch and print users
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)
