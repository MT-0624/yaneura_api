# coding:UTF-8

import random as rd
import time
import os
import responder
import pymysql.cursors

MYSQL_HOSTNAME = "localhost"
MYSQL_USERNAME = "api"
# MYSQL_PASSWORD = os.environ["API_USER_PASSWORD"]
MYSQL_PASSWORD = "api1"


# 形勢判断
def score_to_text(score: int):
    if abs(score) < 100:
        return "互角"

    head = "先手" if score > 0 else "後手"

    score = abs(score)

    stat = {"良し": range(100, 500),
            "有利": range(100, 500),
            "優勢": range(500, 1000),
            "勝勢": range(1000, 1000000)}

    for k, v in stat.items():
        if score in v:
            return f"{head}{k}"
    else:
        return f"{head}勝ち"


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
def demo(req, resp):
    resp.media = {"hello": ""}


@api.route("/analyzer")
async def take_post(req, resp):
    item = await req.media(format="json")
    sfen = item["sfen"]

    with connection.cursor() as cursor:
        sql = f"select get_eval(\"{sfen}\") as score"
        cursor.execute(sql)
        item = cursor.fetchone()
        print(f"fetch {item}")
        cursor.close()
        connection.commit()

    if item["score"] is None:
        with connection.cursor() as cursor:
            sql = f"call insert_request(1,\"{sfen}\",3,100000,20)"
            cursor.execute(sql)
            cursor.close()
            connection.commit()

        item["jap"] = "解析を受け付けました、しばらくお待ち下さい"
        item["score"] = "unanalyzed"
    elif item["score"] == "unanalyzed":
        item["jap"] = "解析中、いましばらくお待ち下さい"
    else:
        item["jap"] = score_to_text(int(item["score"]))

    resp.media = item


if __name__ == '__main__':
    api.run(address='0.0.0.0', port=8080)
