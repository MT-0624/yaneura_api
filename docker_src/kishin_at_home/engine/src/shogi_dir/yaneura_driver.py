# coding:UTF-8

import sys
import os
import random as rd
import time
import datetime as dt
import pymysql.cursors
import copy
import logging

sys.path.append("./ayane")

import shogi.Ayane as ayane

# coding:UTF-8


MYSQL_HOSTNAME = "mysql"
MYSQL_USERNAME = "analyzer"
MYSQL_PASSWORD = os.environ["ENGINE_USER_PASSWORD"]

LOG_PATH = ""
#
# ENGINE_PATH = os.environ["ENGINE_PATH"]
ENGINE_PATH = "/vagrant/shogi_dir/engine/YaneuraOu-by-gcc"

# デバッグ用にエンジンとのやりとり内容を標準出力に出力する。
# usi.debug_print = True


# MySQLに接続する

mysql_setting = {}

logger = logging.getLogger("logger")  # logger名loggerを取得
logger.setLevel(logging.DEBUG)  # loggerとしてはDEBUGで

# handler1を作成
handler1 = logging.StreamHandler()
handler1.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))

# loggerに2つのハンドラを設定
logger.addHandler(handler1)

while True:
    try:
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
        print("Mysql Connection failed")
        time.sleep(1)

if os.path.exists(LOG_PATH):
    # handler2を作成
    handler2 = logging.FileHandler(filename=LOG_PATH)  # handler2はファイル出力
    handler2.setLevel(logging.WARN)  # handler2はLevel.WARN以上
    handler2.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))
    logger.addHandler(handler2)


class Analyzed(object):
    def __init__(self, _score, _sfen, _bestmove, _idea):
        self.score = _score
        self.sfen = _sfen
        self.bestmove = _bestmove
        self.idea = _idea

    def show(self):
        print(f"{self.sfen}")
        print(f"bestmove:{self.bestmove}")
        print(f"idea:{self.idea}")
        print(f"score:{self.score}")
        print()


def fetch_board():
    with connection.cursor() as cursor:
        sql = \
            f"select * from Boards " \
            f" where engine_id = 1 and eval_score = 'unanalyzed'" \
            f" order by request_datetime asc"

        cursor.execute(sql)

        item = cursor.fetchall()
        cursor.close()
        connection.commit()
    return item


# --force-wave-audio
def write_analyzed_result():
    pass


def analyze(sfen, analyze_time=1500):
    logger.info(f"sfen:{sfen}")
    usi = ayane.UsiEngine()

    # エンジンオプション自体は、基本的には"engine_options.txt"で設定する。(やねうら王のdocs/を読むべし)
    # 特定のエンジンオプションをさらに上書きで設定できる
    usi.set_engine_options({
        "Usi_hash": "256",
        "Threads": "1",
        "NetworkDelay": "0",
        "NetworkDelay2": "0",
        "BookFile": "yaneura_book4.db"
    })
    usi.connect(ENGINE_PATH)

    # デバッグ用にエンジンとのやりとり内容を標準出力に出力する。
    usi.debug_print = True

    usi.usi_position(f"{sfen}")

    usi.send_command("multipv 1")
    usi.usi_go_and_wait_bestmove(f"btime 0 wtime 0 byoyomi {analyze_time}")

    # 思考内容を表示させてみる。

    # エンジンを切断
    usi.disconnect()
    logger.info("解析完了")

    """
        self.pv = None  # str
        # 評価値(整数値)
        self.eval = None  # UsiEvalValue
        # 読みの深さ
        self.depth = None  # int
        # 読みの選択深さ
        self.seldepth = None  # int
        # 読みのノード数
        self.nodes = None  # int
        # "go"を送信してからの経過時刻。[ms]
        self.time = None  # int
        # hash使用率 1000分率
        self.hashfull = None  # int
        # nps
        self.nps = None  # int
        # bound
        self.bound = None  # UsiBound
    """

    return copy.deepcopy(usi.think_result.pvs[0])

    # # エンジンを切断
    # usi.disconnect()


def update(_board_id, _an):
    with connection.cursor() as cursor:
        sql = \
            f" update Boards " \
            f" set eval_score = {_an.eval}" \
            f" set nps = {_an.nps}" \
            f" set depth = {_an.depth}" \
            f" where board_id = {_board_id}"

        cursor.execute(sql)
        connection.commit()
    return item


def run():
    it = fetch_board()
    logger.info(f"{len(it)}件が未解析です")

    for item in it:
        an = analyze(item["board"])
        update(item["board_id"], an)
        logger.info(f"[解析]{item['board']}")

    logger.info(f"{len(it)}件解析済")
    return it


if __name__ == '__main__':
    try:
        print(run())
    except KeyboardInterrupt as e:
        logger.info(e)
        connection.close()

