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

            fluger_coins INTEGER DEFAULT 0,

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
            value TEXT,
            item_id INTEGER

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
        await db.execute("""
        CREATE TABLE IF NOT EXISTS news(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            text TEXT,

            author INTEGER,

            date TEXT

        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS fluger_shop(

            id INTEGER PRIMARY KEY,

            name TEXT,

            price INTEGER,

            type TEXT,

            value TEXT

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

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT access
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        user = await cursor.fetchone()

        if user:
            return user["access"]

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

        await db.executemany(
            """
            INSERT OR REPLACE INTO shop
            (id, name, price, type, value)
            VALUES (?, ?, ?, ?, ?)
            """,
            [

                (1, "🔴 Красный ник", 100000, "nick_color", "red"),
                (2, "🟢 Зеленый ник", 100000, "nick_color", "green"),
                (3, "🔵 Синий ник", 100000, "nick_color", "blue"),

                (4, "🥤 Префикс «ШИПУЧКА»", 500000, "prefix", "ШИПУЧКА"),
                (5, "🌪 Префикс «ФЛЮГА»", 1000000, "prefix", "ФЛЮГА"),
                (6, "🪰 Префикс «МУХАА»", 2500000, "prefix", "МУХАА"),
                (7, "😈 Префикс «ДЕМОН»", 5000000, "prefix", "ДЕМОН"),
                (8, "⚡ Префикс «КФГ ФЛЮГЕРА»", 10000000, "prefix", "КФГ ФЛЮГЕРА"),

                (9, "🎁 Кейс FLUGER", 1000000, "case_fluger", "fluger"),
                (10, "💰 Кейс Монет", 500000, "case_money", "money")

            ]
        )

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
async def get_shop_item(item_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "SELECT * FROM shop WHERE id = ?",
            (item_id,)
        )

        return await cursor.fetchone()
async def add_item(user_id, item_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT amount
            FROM inventory
            WHERE user_id=? AND item_id=?
            """,
            (user_id, item_id)
        )

        item = await cursor.fetchone()

        if item:

            await db.execute(
                """
                UPDATE inventory
                SET amount = amount + 1
                WHERE user_id=? AND item_id=?
                """,
                (user_id, item_id)
            )

        else:

            await db.execute(
                """
                INSERT INTO inventory(user_id,item_id,amount)
                VALUES(?,?,1)
                """,
                (user_id, item_id)
            )

        await db.commit()
async def remove_money(user_id, amount):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET balance = balance - ?
            WHERE user_id=?
            """,
            (amount, user_id)
        )

        await db.commit()
async def get_inventory(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT 
                inventory.item_id,
                inventory.amount,
                shop.name,
                shop.type,
                shop.value
            FROM inventory

            JOIN shop
            ON inventory.item_id = shop.id

            WHERE inventory.user_id = ?
            """,
            (user_id,)
        )

        return await cursor.fetchall()
async def use_item(user_id, item_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT shop.*
            FROM inventory
            JOIN shop
            ON inventory.item_id = shop.id
            WHERE inventory.user_id = ?
            AND inventory.item_id = ?
            """,
            (user_id, item_id)
        )

        item = await cursor.fetchone()

        if item is None:
            return None

        if item["type"] == "prefix":

            await db.execute(
                """
                UPDATE users
                SET prefix = ?
                WHERE user_id = ?
                """,
                (item["value"], user_id)
            )

        elif item["type"] == "nick_color":

            await db.execute(
                """
                UPDATE users
                SET nickname_color = ?
                WHERE user_id = ?
                """,
                (item["value"], user_id)
            )

        await db.commit()

        return item
async def remove_item(user_id, item_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT amount
            FROM inventory
            WHERE user_id=? AND item_id=?
            """,
            (user_id, item_id)
        )

        item = await cursor.fetchone()

        if item is None:
            return False


        if item[0] > 1:

            await db.execute(
                """
                UPDATE inventory
                SET amount = amount - 1
                WHERE user_id=? AND item_id=?
                """,
                (user_id, item_id)
            )

        else:

            await db.execute(
                """
                DELETE FROM inventory
                WHERE user_id=? AND item_id=?
                """,
                (user_id, item_id)
            )


        await db.commit()

        return True
async def set_prefix(user_id, prefix):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET prefix=?
            WHERE user_id=?
            """,
            (prefix, user_id)
        )

        await db.commit()
async def add_news(text, author):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT INTO news(text, author, date)
            VALUES(?,?,?)
            """,
            (
                text,
                author,
                datetime.now().strftime("%d.%m.%Y %H:%M")
            )
        )

        await db.commit()



async def get_news():

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM news
            ORDER BY id DESC
            LIMIT 10
            """
        )
async def set_access(user_id, level):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET access = ?
            WHERE user_id = ?
            """,
            (
                level,
                user_id
            )
        )

        await db.commit()

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
                ?, ?, ?
            )
            """,
            (
                user_id,
                username,
                datetime.now().strftime("%d.%m.%Y")
            )
        )

        await db.commit()
async def get_fluger_coins(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT fluger_coins
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = await cursor.fetchone()

        if row:
            return row[0]

        return 0
async def add_fluger_coins(user_id, amount):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET fluger_coins = fluger_coins + ?
            WHERE user_id = ?
            """,
            (
                amount,
                user_id
            )
        )

        await db.commit()
async def remove_fluger_coins(user_id, amount):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET fluger_coins = fluger_coins - ?
            WHERE user_id = ?
            """,
            (
                amount,
                user_id
            )
        )

        await db.commit()
async def fill_fluger_shop():

    async with aiosqlite.connect(DATABASE) as db:

        await db.executemany(
            """
            INSERT OR REPLACE INTO fluger_shop
            (id, name, price, type, value)
            VALUES (?, ?, ?, ?, ?)
            """,
            [

                (
                    1,
                    "👑 КФГ ФЛЮГЕРА",
                    500,
                    "duel_boost",
                    "20"
                ),

                (
                    2,
                    "💰 Денежный буст",
                    100,
                    "reward_boost",
                    "2"
                ),

                (
                    3,
                    "⚔️ Амулет победителя",
                    250,
                    "duel_chance",
                    "15"
                ),

                (
                    4,
                    "🎁 Легендарный кейс",
                    150,
                    "legend_case",
                    "1"
                )

            ]
        )

        await db.commit()
async def get_fluger_shop():

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM fluger_shop
            ORDER BY id
            """
        )

        return await cursor.fetchall()
async def get_fluger_item(item_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM fluger_shop
            WHERE id = ?
            """,
            (item_id,)
        )

        return await cursor.fetchone()
async def remove_fluger_coins(user_id, amount):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET fluger_coins = fluger_coins - ?
            WHERE user_id = ?
            """,
            (
                amount,
                user_id
            )
        )

        await db.commit()
async def get_fluger_inventory(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT 
                inventory.item_id,
                COUNT(inventory.item_id) as amount
            FROM inventory
            WHERE inventory.user_id = ?
            GROUP BY inventory.item_id
            """,
            (user_id,)
        )

        rows = await cursor.fetchall()


        items = []


        names = {

            13: "👑 КФГ ФЛЮГЕРА",

            14: "💰 Денежный буст",

            15: "⚔️ Амулет победителя",

            16: "🎁 Легендарный кейс"

        }


        for row in rows:

            items.append(
                {
                    "name": names.get(
                        row["item_id"],
                        "❓ Неизвестный предмет"
                    ),

                    "amount": row["amount"]
                }
            )


        return items

        return await cursor.fetchall()
async def get_user_item(user_id, item_id):

    async with aiosqlite.connect(DATABASE) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM inventory
            WHERE user_id = ?
            AND item_id = ?
            LIMIT 1
            """,
            (
                user_id,
                item_id
            )
        )

        return await cursor.fetchone()
async def remove_item(user_id, item_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT rowid
            FROM inventory
            WHERE user_id = ?
            AND item_id = ?
            LIMIT 1
            """,
            (
                user_id,
                item_id
            )
        )

        row = await cursor.fetchone()

        if row:

            await db.execute(
                """
                DELETE FROM inventory
                WHERE rowid = ?
                """,
                (
                    row[0],
                )
            )

        await db.commit()
