import datetime
import random
import json
import time
import requests as r


if __name__ == '__main__':
    ind = 0
    while ind < 70:
        r.post(
            url = 'http://127.0.0.1:8000/send/jvm-memory',
            data = json.dumps({
                'value': random.randint(9*2**30, 40*2**30),
                'date': datetime.datetime(year=2024, month=12, day=26, hour=20, minute=ind, second=0).timestamp(),
                'instance': 'HOST-1'
            })
        )

        r.post(
            url = 'http://127.0.0.1:8000/send/jvm-memory',
            data = json.dumps({
                'value': random.randint(24*2**30, 65*2**30),
                'date': datetime.datetime(year=2024, month=12, day=26, hour=20, minute=ind, second=0).timestamp(),
                'instance': 'HOST-2'
            })
        )

        r.post(
            url = 'http://127.0.0.1:8000/send/jvm-memory',
            data = json.dumps({
                'value': random.randint(256*2**20, 1200*2**20),
                'date': datetime.datetime(year=2024, month=12, day=26, hour=20, minute=ind, second=0).timestamp(),
                'instance': 'HOST-3'
            })
        )

        ind += 10
        time.sleep(9)

