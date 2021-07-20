# coding:UTF-8

from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

import sys, queue, yaml

sys.path.append("../Ayane-master/source")

import shogi.Ayane as ayane

app = FastAPI()

with open("./engine_option.yml", "r") as f:
    ENGINE_SETTING = yaml.safe_load(f)

engine = ayane.UsiEngine()
engine.set_engine_options(ENGINE_SETTING)

path = r"/home/vagrant/shogi_dir/YaneuraOu-by-gcc"

engine.connect(path)

"""
仮想環境上で実行することを想定したファイルのため
pycharmなどで書くときはinterpreterをリモートのマシンのpython3に設定すること
実行は.pyのある場所で
uvicorn main:app --reload
"""



class Query(BaseModel):
    sfen: str
    time_limit: int
    depth_limit: int


@app.post('/query/', status_code=202)
async def start(query: Query):

    return {"message": "時間のかかる処理を受け付けました"}


@app.get('/health_check/', status_code=200)
async def health_check():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
