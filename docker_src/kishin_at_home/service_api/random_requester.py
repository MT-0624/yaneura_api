# coding:UTF-8

import sys
import random as rd
import time

MYSQL_HOSTNAME = ""
MYSQL_USERNAME = ""
MYSQL_PASSWORD = ""

RANDOM_SFEN = True
index = 0

with open("./huge_sfen.txt", encoding="UTF-8") as f:
    sfen_lst = f.read().split("\n")[:-2]

while True:
    wait = rd.randint(2, 5) + rd.randint(2, 5)
    time.sleep(wait)

    print(wait)
    if RANDOM_SFEN:
        print(rd.choice(sfen_lst))
    else:
        print(sfen_lst[index])
        index += 1
