import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > ?', (40,)) as cursor:
            older_users = await cursor.fetchall()
            return older_users

def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

asyncio.run(fetch_concurrently())
