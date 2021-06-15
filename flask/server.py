# coding:UTF-8

from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from time import sleep
from typing import Dict
import uvicorn

import sys, queue

sys.path.append("../Ayane-master/source")

import shogi.Ayane as ayane

app = FastAPI()

engine = ayane.UsiEngine()
engine.set_engine_options()

"""
仮想環境上で実行することを想定したファイルのため
pycharmなどで書くときはinterpreterをリモートのマシンのpython3に設定すること
実行は.pyのある場所で
uvicorn main:app --reload
"""


class Job(BaseModel):
    job_id: int
    is_cancelled: bool = False

    def __call__(self):
        jobs[self.job_id] = self
        try:
            for _ in range(10):
                print(f'{datetime.now():%H:%M:%S}')
                sleep(1)

                if self.is_cancelled:
                    del jobs[self.job_id]
                    break

        finally:
            print('時間のかかる処理が終わりました')


jobs: Dict[int, Job] = {}


@app.post('/{job_id}/', status_code=202)
async def start(job_id: int, background_tasks: BackgroundTasks):
    t = Job(job_id=job_id)
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
