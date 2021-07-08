# coding:UTF-8

import random as rd
import time
import os
import pymysql.cursors

time.sleep(60)

MYSQL_HOSTNAME = "mysql"
MYSQL_USERNAME = "api"
MYSQL_PASSWORD = os.environ["API_USER_PASSWORD"]
# MySQLに接続する
connection = pymysql.connect(host=MYSQL_HOSTNAME,
                             port=3306,
                             user=MYSQL_USERNAME,
                             password=MYSQL_PASSWORD,
                             db='kishin_service',
                             charset='utf8',
                             # cursorclassを指定することで
                             # Select結果をtupleではなくdictionaryで受け取れる
                             cursorclass=pymysql.cursors.DictCursor)

RANDOM_SFEN = True
index = 0

with open("./huge_sfen.txt", encoding="UTF-8") as f:
    sfen_lst = f.read().split("\n")[:-2]


def execution(sfen):
    with connection.cursor() as cursor:
        sql = f"call insert_request(1,\"{sfen}\",3,100000,20)"
        cursor.execute(sql)
        print(sql)
        cursor.close()
        connection.commit()


while True:
    wait = rd.randint(1, 3) + rd.randint(1, 3)
    time.sleep(wait)

    if RANDOM_SFEN:
        sfen = rd.choice(sfen_lst)
    else:
        sfen = sfen_lst[index]
        index += 1
    execution(sfen)
