import mysql.connector
from mysql.connector import errorcode
from decimal import Decimal
import numpy as np
default_Table_des = "(  `id` INT UNSIGNED AUTO_INCREMENT," \
                    "  `t` FLOAT NOT NULL," \
                    "  `pcd` BLOB," \
                    "  `id_max` INT UNSIGNED, " \
                    "  PRIMARY KEY (`id`)" \
                    ")ENGINE =MyISAM DEFAULT CHARSET 'utf8'"

default_Inf_des = "(t, pcd) " \
                  "VALUES " \
                  "(%s, %s)"

zero_Inf_des = "(t, pcd, id_max)" \
               "VALUES " \
               "(%s, %s, %s)"


def create_database(cursor, db_name):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8' ".format(db_name))
    except mysql.connector.Error as err:
        print("\033[31m [ERROR] Failed to create database:{} \033[31m".format(db_name))
        exit(1)


class ProsDataDB():
    def __init__(self, db_name):
        self.cnx = mysql.connector.connect(
            user='root',
            password='Wyx@740214'
        )
        self.cursor = self.cnx.cursor(buffered=True)
        self.row_id = 0
        try:
            self.cursor.execute("USE {}".format(db_name))
        except mysql.connector.Error as err:
            print("Database {} doesn't exists.".format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(self.cursor, db_name)
                print("Database {} created successfully".format(db_name))
                self.cnx.database = db_name
            else:
                print(err)
                exit(1)
        self.TABLES = {}
        self.cursor.execute("SHOW TABLES;")
        val = self.cursor.fetchall()
        for i in range(len(val)):
            table_name = val[i][0]
            self.TABLES[table_name] = ["db_" + table_name]

    def add_Table(self, table_name, table_des=default_Table_des):
        self.TABLES[table_name] = ("CREATE TABLE {} {}".format(table_name, table_des))
        self.table_name = table_name
        try:
            self.cursor.execute(self.TABLES[table_name])
            print("TABLE {} created successfully".format(table_name))
            ins_des = ("INSERT INTO {} {}".format(self.table_name, zero_Inf_des))
            zeros_fill = np.zeros([100,2]).astype(np.float32)
            self.cursor.execute(ins_des, ([0, zeros_fill.tobytes(), 1]))
            self.cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("TABLE {} already exists".format(table_name))
            else:
                print(err.msg)

    def insert_Info(self, inf_values, inf_des=default_Inf_des):
        t = inf_values['t']
        pcd = inf_values['pcd']
        ins_des = ("INSERT INTO {} {};".format(self.table_name, inf_des))
        try:
            self.cursor.execute(ins_des, ([t, pcd]))
            self.cnx.commit()
            self.row_id = self.cursor.lastrowid
            self.cursor.execute("UPDATE {} SET `id_max`={} WHERE `id` = 1;".format(self.table_name, self.row_id))
            print('Insert id {}'.format(self.row_id))
        except mysql.connector.Error as err:
            print(err.msg)

    def get_last_id(self):
        self.cursor.execute("SELECT `id_max` FROM {} WHERE `id`= 1;".format(self.table_name))
        val = self.cursor.fetchone()
        self.row_id = val[0]
        return self.row_id

    def fetch_Info(self, col_name="`t`,`pcd`"):
        sel_des = ("SELECT {} FROM {} WHERE `id` = %s;".format(col_name, self.table_name))
        self.cursor.execute(sel_des, ([self.get_last_id()]))
        print('Fetch id {}'.format(self.row_id))
        return self.cursor.fetchall()

    def delete_Tables(self, table_name_list):
        for table_name in table_name_list:
            drop_des = ("DROP TABLE IF EXISTS {};".format(table_name))
            self.cursor.execute(drop_des)

    def close_DB(self):
        self.cursor.close()
        self.cnx.close()
