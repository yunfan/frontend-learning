#!/usr/bin/env python3
# coding: utf-8

import sys
import asyncio
import websockets
import json

BrLock = asyncio.Lock()
Room = set()      ## TODO weakref problem

async def handler(ws, path):
    print(dir(ws), file=sys.stderr)
    if len(Room) >= 100:
      await ws.send(json.dumps({'code': 1, 'msg': 'this chatroom is full'}))
      await ws.close()
    else:
      ## broadcast the new client
      with await BrLock:
        for conn in Room:
          await conn.send(json.dumps({'code': -1, 'msg': 'new client join'}))
        Room.add(ws)

      ## loop iterate all the incomming message
      async for msg in ws:
        with await BrLock:
          for conn in Room:
            await conn.send(json.dumps({'code': -2, 'msg': msg}))

      ## broadcast client's quit
      with await BrLock:
        for conn in Room:
          await conn.send(json.dumps({'code': 2, 'msg': 'client has quited now'}))

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(handler, 'localhost', 5678))
    loop.run_forever()

if '__main__' == __name__:
    main()
