import sqlite3

from . import settings


connection = sqlite3.connect(settings.DATABASE_URL)
cursor = connection.cursor()


def init_db():
    sql = "CREATE TABLE IF NOT EXISTS {0} ({1});".format(
        settings.TABLE_NAME_JVM_MEMORY,
        ','.join([f'{key} {value}' for key, value in settings.COLS_JVM_MEMORY.items()])
    )
    cursor.execute(sql)


def close_db():
    connection.close()
