# coding:UTF-8

import random as rd
import time
import os
import responder
import pymysql.cursors

MYSQL_HOSTNAME = "mysql"
MYSQL_USERNAME = "api"
MYSQL_PASSWORD = os.environ["API_USER_PASSWORD"]

api = responder.API()

while True:
    try:
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

        break
    except Exception as e:
        print(e)
        time.sleep(60)

RANDOM_SFEN = True
index = 0

with open("./huge_sfen.txt", encoding="UTF-8") as f:
    sfen_lst = f.read().split("\n")[:-2]


@api.route("/")
def test(req, resp):
    resp.media = {"hello":""}


@api.route("/analyzer")
async def take_post(req, resp):
    if req.method == "get":
        with connection.cursor() as cursor:
            sql = f"call insert_request(1,\"{sfen}\",3,100000,20)"
            cursor.execute(sql)
            print(sql)
            cursor.close()
            connection.commit()
        resp.text = "please send post"
    else:
        data = await req.media()

        with connection.cursor() as cursor:
            print(data)
            sql = f"select get_eval(\"{data}\")"
            cursor.execute(sql)
            score = cursor.fetchall()
            print(f"fetch {score}")
            cursor.close()
            connection.commit()

        resp.text = f"{score}"

    resp.media = str(score)


if __name__ == '__main__':
    api.run()
