import aiosqlite
from datetime import datetime
import time


DATABASE = "database.db"



async def create_database():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(

            user_id INTEGER PRIMARY KEY,

            username TEXT,

            nickname TEXT DEFAULT '',

            nickname_color TEXT DEFAULT '',

            prefix TEXT DEFAULT '',

            role TEXT DEFAULT 'Новый эдитор',

            access INTEGER DEFAULT 1,

            balance INTEGER DEFAULT 0,

            messages INTEGER DEFAULT 0,

            joined TEXT

        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS mutes(

            user_id INTEGER,

            until INTEGER,

            reason TEXT

        )
        """)


        await db.commit()
        await db.execute("""
        CREATE TABLE IF NOT EXISTS bans(

            user_id INTEGER PRIMARY KEY,

            admin_id INTEGER,

            reason TEXT,

            ban_date TEXT

        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tempbans (

            user_id INTEGER PRIMARY KEY,

            admin_id INTEGER,

            reason TEXT,

            until INTEGER

        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS businesses(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            income INTEGER,
            balance INTEGER DEFAULT 0

        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS rewards(

            user_id INTEGER PRIMARY KEY,
            last_reward INTEGER

        )
        """)
        await db.commit()

        # Создаем владельца, если его еще нет
        await db.execute("""
        INSERT OR IGNORE INTO users (
            user_id,
            username,
            joined
        )
        VALUES (?, ?, ?)
        """, (
            7798920511,
            "",
            datetime.now().strftime("%d.%m.%Y")
        ))

        # Выдаем 4 уровень доступа
        await db.execute("""
        UPDATE users
        SET access = 4
        WHERE user_id = ?
        """, (7798920511,))

        await db.commit()
        # Магазин
        await db.execute("""
        CREATE TABLE IF NOT EXISTS shop(

            id INTEGER PRIMARY KEY,
            name TEXT,
            price INTEGER,
            type TEXT,
            value TEXT

        )
        """)

        # Инвентарь
        await db.execute("""
        CREATE TABLE IF NOT EXISTS inventory(

            user_id INTEGER,
            item_id INTEGER,
            amount INTEGER DEFAULT 1

        )
        """)




async def add_user(user_id, username):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
        """
        INSERT OR IGNORE INTO users
        (
        user_id,
        username,
        joined
        )

        VALUES
        (
        ?,
        ?,
        datetime('now')
        )

        """,
        (
        user_id,
        username
        )
        )


        await db.commit()




async def get_user(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row


        cursor = await db.execute(
        """
        SELECT * FROM users
        WHERE user_id=?
        """,
        (user_id,)
        )


        user = await cursor.fetchone()


        return user




async def add_message(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
        """
        UPDATE users

        SET messages = messages + 1

        WHERE user_id=?

        """,
        (user_id,)
        )


        await db.commit()




async def get_balance(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
        """
        SELECT balance
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
        )


        result = await cursor.fetchone()


        if result:

            return result[0]


        return 0




async def remove_money(user_id, amount):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET balance = balance - ?

            WHERE user_id=?
            """,
            (
                amount,
                user_id
            )
        )

        await db.commit()



async def get_user_by_username(username):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row


        cursor = await db.execute(
            """
            SELECT * FROM users

            WHERE username=?
            """,
            (
                username,
            )
        )


        user = await cursor.fetchone()


        return user
async def add_money(user_id, amount):

    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            """
            UPDATE users

            SET balance = balance + ?

            WHERE user_id=?
            """,
            (
                amount,
                user_id
            )
        )

        await db.commit()
async def set_nickname(user_id, nickname):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET nickname=?

            WHERE user_id=?
            """,
            (
                nickname,
                user_id
            )
        )

        await db.commit()



async def remove_nickname(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET nickname=''

            WHERE user_id=?
            """,
            (
                user_id,
            )
        )

        await db.commit()



async def get_nicknames():

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row


        cursor = await db.execute(
            """
            SELECT username, nickname

            FROM users

            WHERE nickname != ''
            """
        )


        users = await cursor.fetchall()


        return users
async def get_access(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT access
            FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )

        result = await cursor.fetchone()


        if result:
            return result[0]


        return 1


        result = await cursor.fetchone()


        if result:

            return result[0]


        return 1

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT access

            FROM users

            WHERE user_id=?
            """,
            (
                user_id,
            )
        )


        result = await cursor.fetchone()


        if result:
            return result[0]


        return 1
async def change_access(user_id, level):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET access=?

            WHERE user_id=?
            """,
            (
                level,
                user_id
            )
        )

        await db.commit()
async def set_role(user_id, role):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET role=?

            WHERE user_id=?
            """,
            (
                role,
                user_id
            )
        )

        await db.commit()
async def get_profile(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM users
            WHERE user_id=?
            """,
            (
                user_id,
            )
        )


        user = await cursor.fetchone()


        return user
async def add_mute(user_id, until, reason):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT INTO mutes
            (
            user_id,
            until,
            reason
            )

            VALUES
            (?,?,?)
            """,
            (
                user_id,
                until,
                reason
            )
        )


        await db.commit()
async def get_mute(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM mutes
            WHERE user_id=?
            """,
            (
                user_id,
            )
        )


        return await cursor.fetchone()

async def remove_mute(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            "DELETE FROM mutes WHERE user_id=?",
            (user_id,)
        )

        await db.commit()

async def add_ban(user_id, admin_id, reason):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT OR REPLACE INTO bans
            (
                user_id,
                admin_id,
                reason,
                ban_date
            )

            VALUES (?,?,?,?)
            """,
            (
                user_id,
                admin_id,
                reason,
                datetime.now().strftime("%d.%m.%Y %H:%M")
            )
        )

        await db.commit()

async def is_banned(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT user_id
            FROM bans
            WHERE user_id=?
            """,
            (user_id,)
        )

        return await cursor.fetchone()

async def remove_ban(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            DELETE FROM bans
            WHERE user_id=?
            """,
            (user_id,)
        )

        await db.commit()


async def add_tempban(user_id, admin_id, reason, until):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT OR REPLACE INTO tempbans
            (
                user_id,
                admin_id,
                reason,
                until
            )
            VALUES (?,?,?,?)
            """,
            (
                user_id,
                admin_id,
                reason,
                until
            )
        )

        await db.commit()


async def is_tempbanned(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM tempbans
            WHERE user_id=?
            """,
            (user_id,)
        )

        ban = await cursor.fetchone()

        if ban is None:
            return False

        if ban["until"] > int(time.time()):
            return True


        await db.execute(
            "DELETE FROM tempbans WHERE user_id=?",
            (user_id,)
        )

        await db.commit()

        return False


async def get_bans(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM bans
            WHERE user_id=?
            """,
            (user_id,)
        )

        bans = await cursor.fetchall()

        return bans
async def remove_tempban(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            DELETE FROM tempbans
            WHERE user_id=?
            """,
            (user_id,)
        )

        await db.commit()
async def get_tempbans(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM tempbans
            WHERE user_id=?
            """,
            (user_id,)
        )

        tempbans = await cursor.fetchall()

        return tempbans
async def set_access(user_id, access):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET access=?
            WHERE user_id=?
            """,
            (
                access,
                user_id
            )
        )

        await db.commit()
async def get_staff():

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT username, role, access
            FROM users
            WHERE access >= 2
            ORDER BY access DESC
            """
        )

        return await cursor.fetchall()
async def get_businesses(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM businesses
            WHERE user_id=?
            """,
            (user_id,)
        )

        return await cursor.fetchall()
async def add_business(user_id, name, income):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT INTO businesses
            (
                user_id,
                name,
                income
            )

            VALUES (?,?,?)
            """,
            (
                user_id,
                name,
                income
            )
        )

        await db.commit()
async def get_business_info(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM businesses
            WHERE user_id=?
            """,
            (user_id,)
        )

        return await cursor.fetchall()
async def collect_business_money(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT SUM(balance)
            FROM businesses
            WHERE user_id=?
            """,
            (user_id,)
        )

        result = await cursor.fetchone()

        money = result[0] or 0


        if money > 0:

            await db.execute(
                """
                UPDATE businesses
                SET balance=0
                WHERE user_id=?
                """,
                (user_id,)
            )

        await db.commit()

        return money
async def add_business_income():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE businesses
            SET balance = balance + income
            """
        )

        await db.commit()
async def get_reward_time(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT last_reward
            FROM rewards
            WHERE user_id=?
            """,
            (user_id,)
        )

        return await cursor.fetchone()



async def set_reward_time(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT OR REPLACE INTO rewards
            (
                user_id,
                last_reward
            )
            VALUES (?,?)
            """,
            (
                user_id,
                int(time.time())
            )
        )

        await db.commit()
async def add_business_income():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE businesses
            SET balance = balance + income
            """
        )

        await db.commit()
async def add_money(user_id, amount):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE user_id = ?
            """,
            (amount, user_id)
        )

        await db.commit()
async def fill_shop():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        INSERT OR IGNORE INTO shop (id, name, price, type, value)
        VALUES
        (1, '🔴 Красный ник', 100000, 'nickname_color', '🔴'),
        (2, '🔵 Синий ник', 100000, 'nickname_color', '🔵'),
        (3, '🟢 Зеленый ник', 100000, 'nickname_color', '🟢'),
        (4, '🟣 Фиолетовый ник', 150000, 'nickname_color', '🟣'),

        (5, '👑 VIP', 500000, 'prefix', '👑 VIP'),
        (6, '💎 ELITE', 1000000, 'prefix', '💎 ELITE'),
        (7, '🔥 LEGEND', 2500000, 'prefix', '🔥 LEGEND'),
        (8, '⚡ OWNER', 5000000, 'prefix', '⚡ OWNER')
        """)

        await db.commit()
async def get_shop():

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT *
        FROM shop
        ORDER BY id
        """)

        return await cursor.fetchall()
