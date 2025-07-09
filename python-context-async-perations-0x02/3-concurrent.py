import aiosqlite
import asyncio

DB_NAME = 'users.db'

# ✅ Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users  # ✅ required

# ✅ Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users  # ✅ required

# ✅ Run both fetches concurrently and print results
async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for user in users:
        print(user)

    print("\nUsers Older Than 40:")
    for user in older_users:
        print(user)

# ✅ Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
