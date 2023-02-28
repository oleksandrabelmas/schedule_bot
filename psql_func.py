from bots_data import *

import psycopg2


def insert_func(user_tg_id, user_name, user_class):
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME,
        )

        connection.autocommit = True

        cursor = connection.cursor()

        # створюємо табличку якщо немає
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS users(
            user_tg_id varchar(50) PRIMARY KEY,
            user_name varchar(50) NOT NULL,
            user_class varchar(10) NOT NULL
            );"""
        )

        # додаємо данні
        cursor.execute(
            f"""
            INSERT INTO users (user_tg_id, user_name, user_class) VALUES
            ({user_tg_id}, '{user_name}', '{user_class}');
            """
        )

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            cursor.close()
            connection.close()


def select_func(user_tg_id):
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME,
        )

        connection.autocommit = True

        cursor = connection.cursor()

        # перевіряємо чи користувач вже зареєстрований
        cursor.execute(
            f"""
            SELECT * FROM users 
            WHERE user_tg_id = '{user_tg_id}';
            """
        )

        if cursor.fetchone():
            return True

        else:
            return False

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            cursor.close()
            connection.close()