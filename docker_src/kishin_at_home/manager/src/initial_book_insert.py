# coding:UTF-8

import os
import pymysql
import time

ROOT_PASSWORD = os.environ["MYSQL_ROOT_PASSWORD"]
API_USER_PASSWORD = os.environ["API_USER_PASSWORD"]
ENGINE_USER_PASSWORD = os.environ["ENGINE_USER_PASSWORD"]

queries = [
    f"create user 'analyzer'@'%' identified by '{ENGINE_USER_PASSWORD}';",
    f"create user 'api'@'%' identified by '{API_USER_PASSWORD}';",
    f"grant execute on procedure kishin_service.insert_request to 'api'@'%';",
    f"grant select,update on kishin_service.Boards to 'analyzer'@'%';",
]
while True:
    try:
        connection = pymysql.connect(host="mysql",
                                     port=3306,
                                     user="root",
                                     password=ROOT_PASSWORD,
                                     db='kishin_service',
                                     charset='utf8',
                                     # cursorclassを指定することで
                                     # Select結果をtupleではなくdictionaryで受け取れる
                                     cursorclass=pymysql.cursors.DictCursor)

        for q in queries:
            with connection.cursor() as cursor:
                cursor.execute(q)
                print(q)
                cursor.close()
                connection.commit()

        print("Initialization completed!!")
        exit()
    except Exception as e:
        print(e)
    finally:
        time.sleep(15)