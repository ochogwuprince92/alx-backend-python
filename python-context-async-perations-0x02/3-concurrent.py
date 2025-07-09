import aiosqlite
import asyncio

DB_NAME = 'users.db'

# ✅ Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All Users:")
            for user in users:
                print(user)

# ✅ Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers Older Than 40:")
            for user in older_users:
                print(user)

# ✅ Run both fetches concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# ✅ Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
