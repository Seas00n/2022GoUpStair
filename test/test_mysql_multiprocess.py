import time

from utils.data_db import *
import numpy as np
from multiprocessing import Process, Manager
from datetime import datetime
from contextlib import contextmanager
import random


@contextmanager
def mysql_connect(db_name):
    DB = ProsDataDB(db_name)
    yield DB
    DB.close_DB()


def main():
    now = datetime.now()
    table_name = now.strftime("data%m_%d_%H_%M_%S")
    db_name = 'Test_DB'

    with mysql_connect(db_name) as DB:
        print(f'Create Database{db_name}')
        DB.add_Table(table_name)
        process_client = Process(target=client_task, args=(db_name, table_name))
        process_server = Process(target=server_task, args=(db_name, table_name))
        process_client.start()
        process_server.start()
        for i in range(50):
            print("Num of row:{}".format(DB.get_last_id()))
            time.sleep(0.1)
        process_client.join()
        process_server.join()

def client_task(db_name, table_name):
    print("Create Cursor")
    with mysql_connect(db_name) as DB:
        DB.add_Table(table_name)
        t0 = time.time()
        for i in range(50):
            inf_des = {}
            inf_des['t'] = time.time() - t0
            l = random.randint(1000, 7000)
            pcd_2d = np.random.random([l, 2]).astype(np.float32)
            inf_des['pcd'] = pcd_2d.tobytes()
            DB.insert_Info(inf_des)
            time.sleep(0.2)
    print('Process Client Over')


def server_task(db_name, table_name):
    print("Create Server")
    with mysql_connect(db_name) as DB:
        DB.add_Table(table_name)
        for i in range(50):
            value = DB.fetch_Info()
            if value is None:
                print("No Data")
            else:
                t = value[0][0]
                pcd = np.frombuffer(value[0][1], dtype=np.float32)
            time.sleep(0.4)
    print('Process Server Over')

if __name__ == '__main__':
    main()
