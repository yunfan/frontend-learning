#!/usr/bin/env python3
# coding: utf-8

import sys
import asyncio
import websockets
import json

from copy import copy

BrLock = asyncio.Lock()
Room = set()      ## TODO weakref problem

async def handler(ws, path):
    print(dir(ws), file=sys.stderr)
    username = ws.remote_address
    if len(Room) >= 100:
      await ws.send(json.dumps({'code': 1, 'msg': 'this chatroom is full'}))
      await ws.close()
    else:
      ## broadcast the new client
      with await BrLock:
        for conn in copy(Room):
          await conn.send(json.dumps({'code': -1, 'msg': 'new client join', 'user': username}))
        Room.add(ws)

      ## loop iterate all the incomming message
      async for msg in ws:
        with await BrLock:
          for conn in copy(Room):
            ##if not conn.writer_is_closing:
                await conn.send(json.dumps({'code': -2, 'msg': msg, 'user': username}))
            ##else:
            ##    try:
            ##        Room.remove(conn)
            ##    except:
            ##        pass

      ## broadcast client's quit
      with await BrLock:
        for conn in copy(Room):
          await conn.send(json.dumps({'code': 2, 'msg': 'client has quited now', 'user': username}))

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(handler, 'localhost', 5678))
    loop.run_forever()

if '__main__' == __name__:
    main()
