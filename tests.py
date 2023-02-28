from bots_data import *

import psycopg2


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
            print('success')


select_data(5146241627)
