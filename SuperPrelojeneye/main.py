from fastapi import FastAPI, Request, Response
from SuperPrelojeneye.Api.ApiPost.GetPost import man_router
import time
from typing import Callable
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(man_router)

responeurls = {}

Limit = 100
stime = 60

@app.middleware("http")
async def my_middleware(request: Request, call_next: Callable):
    ip_address = request.client.host
    start = time.time()

    if not ip_address in responeurls:
        responeurls[ip_address] = []

    responeurls[ip_address] = [
        t for t in responeurls[ip_address] if start - t < stime
    ]

    if len(responeurls[ip_address]) >= Limit:
        return Response(status_code=429, content="TE CHO DELAESH!")

    responeurls[ip_address].append(start)

    response = await call_next(request)
    return response

