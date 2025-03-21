import aiosqlite
import datetime as dt

async def get_conn():
    conn = await aiosqlite.connect("database.db")
    return conn

async def close_connection(conn):
    await conn.close()

async def create_table_users(conn):
    await conn.execute("""CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY NOT NULL,
    registration_date TEXT NOT NULL,
    scores INTEGER NOT NULL
    )""")
    await conn.commit()

async def create_table_completed_tasks(conn):
    await conn.execute("PRAGMA foreign_keys = ON")
    await conn.execute("""CREATE TABLE IF NOT EXISTS Completed_tasks (
    task_id INTEGER,
    user_complete_id INTEGER NOT NULL,
    FOREIGN KEY (user_complete_id) REFERENCES Users(user_id)
    )""")
    await conn.commit()

async def new_user(user_id):
    conn = await get_conn()
    date = dt.date.today()
    await conn.execute("INSERT OR IGNORE INTO Users (user_id, registration_date, scores) VALUES (?, ?, ?)", (user_id, date, 0,))
    await conn.commit()
    await close_connection(conn)

async def is_user_already_registered(user_id):
    conn = await get_conn()
    async with conn.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)) as cursor:
        if (await cursor.fetchone() is None):
            return False
        else:
            return True
    await close_connection(conn)

async def is_task_completed(conn, user_id, task_id):
    async with conn.execute("SELECT * FROM Completed_tasks WHERE user_complete_id = ? AND task_id = ?", (user_id, task_id,)) as cursor:
        if (await cursor.fetchone() is None):
            return False
        else:
            return True

async def user_complete_the_task(conn, user_id, task_id):
    await conn.execute("INSERT INTO Completed_tasks (task_id, user_complete_id) VALUES (?, ?)", (task_id, user_id,))
    await conn.commit()

async def get_registration_date(user_id):
    conn = await get_conn()
    async with conn.execute("SELECT registration_date FROM Users WHERE user_id = ?", (user_id,)) as cursor:
        data = await cursor.fetchall()
    await close_connection(conn)
    return data