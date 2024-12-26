import os

##############################################################
# Server
##############################################################

LISTEN_HOST = '127.0.0.1'
LISTEN_PORT = 8000

PATH_TO_GET_PREVIOUS_3_HOURS_JVM_MEMORY_DATA = '/jvm-memory/3'

PATH_TO_SEND_JVM_MEMORY_DATA = '/send/jvm-memory'

# ... in seconds
TIMSTAMP_DIFF = 0

##############################################################
# Database
##############################################################

DATABASE_NAME = 'db.sql'
DATABASE_DIRECTORY_NAME = 'db'
DATABASE_URL = os.path.join(os.getcwd(), DATABASE_DIRECTORY_NAME, DATABASE_NAME)

TABLE_NAME_JVM_MEMORY = 'jvm_memory'
COLS_JVM_MEMORY = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'value': 'INTEGER',
    'date': 'INTEGER',
    'instance': 'TEXT'
}

##############################################################
# Scheduler
##############################################################
