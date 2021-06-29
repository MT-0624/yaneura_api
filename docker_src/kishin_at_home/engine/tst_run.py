# coding:UTF-8

import os
import pymysql.cursors
import random

# MySQLに接続する
connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             db='sample',
                             charset='utf8',
                             # cursorclassを指定することで
                             # Select結果をtupleではなくdictionaryで受け取れる
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "SELECT board_id ,board FROM user WHERE age >= 50"
    cursor.execute(sql)

    # Select結果を取り出す
    results = cursor.fetchall()
    for r in results:
        print(r)
        # => {'name': 'Cookie', 'id': 3}

# MySQLから切断する
connection.close()
