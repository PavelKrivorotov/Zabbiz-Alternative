import json
from datetime import timedelta

from . import settings
from .database import connection, cursor


def create_jvm_memory_object(raw: bytes):
    data: dict = json.loads(raw)
    sql = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(
        settings.TABLE_NAME_JVM_MEMORY,
        ",".join(list(settings.COLS_JVM_MEMORY.keys())[1:]),
        "'{0}','{1}','{2}'".format(
            data.get('value', 'null'),
            data.get('date', 'null'),
            data.get('instance', 'null')
        )
    )
    cursor.execute(sql)
    connection.commit()

def get_jvm_memory_objects(instance: str, hours: int = 3, days: int = 0):
    interval = timedelta(days=days, hours=hours)
    sql = """
        SELECT
            value,
            date
        FROM {0}
        WHERE
            instance = '{1}' AND
            date >= (strftime('%s', 'now') - {2} + {3})
        ORDER BY
            id
    """.format(
        settings.TABLE_NAME_JVM_MEMORY,
        instance,
        interval.total_seconds(),
        settings.TIMSTAMP_DIFF
    )

    data = cursor.execute(sql)
    return data.fetchall()


# "SELECT value, date FROM jvm_memory WHERE instance = '' AND date >= (strftime('%s', 'now') - ) ORDER BY id DESC"


