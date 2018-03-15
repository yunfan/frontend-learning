#!/usr/bin/env python3
# coding: utf-8

import sys
import asyncio
import websockets
import json

from copy import copy

from websockets.exceptions import ConnectionClosed

BrLock = asyncio.Lock()
Room = set()      ## TODO weakref problem

async def broadcast(msg):
    with await BrLock:
        new_room = set()
        for conn in Room:
            try:
                await conn.send(msg)
                new_room.add(conn)
            except ConnectionClosed as ex:
                pass

        Room.clear()
        Room.update(new_room)

async def handler(ws, path):
    ##print(dir(ws), file=sys.stderr)
    username = ws.remote_address
    if len(Room) >= 100:
      await ws.send(json.dumps({'code': 1, 'msg': 'this chatroom is full'}))
      await ws.close()
    else:
      ## broadcast the new client
      await broadcast(json.dumps({'code': -1, 'msg': 'new client join', 'user': username}))
      with await BrLock:
          Room.add(ws)

      ## loop iterate all the incomming message
      try:
          async for msg in ws:
              await broadcast(json.dumps({'code': -2, 'msg': msg, 'user': username}))
      except ConnectionClosed as ex:
          try:
              with await BrLock:
                  Room.remove(ws)
          except:
              pass

      ## broadcast client's quit
      await broadcast(json.dumps({'code': 2, 'msg': 'client has quited now', 'user': username}))

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(handler, 'localhost', 5678))
    loop.run_forever()

if '__main__' == __name__:
    main()
