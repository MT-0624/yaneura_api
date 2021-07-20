# coding:UTF-8

from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from time import sleep
from typing import Dict
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


class Job(BaseModel):
    job_id: int
    query: Query
    is_cancelled: bool = False

    def __call__(self):
        jobs[self.job_id] = self
        try:
            engine.connect(path)
            engine.usi_position(self.query.sfen)
            engine.usi_go_and_wait_bestmove(f"btime 0 wtime 0 byoyomi {self.query.time_limit * 1000}")
            print(f"=== UsiThinkResult{self.job_id} ===\n" + engine.think_result.to_string())
            engine.disconnect()
        finally:
            print(f'{self.job_id}>処理が終わりました')


jobs: Dict[int, Job] = {}


@app.post('/{job_id}/', status_code=202)
async def start(job_id: int, background_tasks: BackgroundTasks, query: Query):
    t = Job(job_id=job_id, query=query)
    background_tasks.add_task(t)
    return {"message": "時間のかかる処理を受け付けました"}


@app.delete('/{job_id}/', status_code=202)
async def stop(job_id: int):
    t = jobs.get(job_id)
    if t is None:
        raise HTTPException(400, detail="job is not exists.")

    jobs[job_id].is_cancelled = True
    return {"message": f"{job_id}の中止処理を受け付けました"}


@app.get('/{job_id}/', status_code=200)
async def status(job_id: int):
    if job_id in jobs:
        return {"message": f"{job_id}は実行中です"}
    else:
        return {"message": f"{job_id}は実行していません"}


@app.get('/health_check/', status_code=200)
async def health_check():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
