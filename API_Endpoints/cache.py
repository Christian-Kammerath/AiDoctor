from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import APIRouter
import asyncio
import apiBaseClasses

router = APIRouter()

cache = {}


# can use Websocket to return continuously changing data from cache.
@router.websocket("/cache/socket/{id}")
async def websocket_endpoint(websocket: WebSocket, id: str):
    await websocket.accept()
    try:
        while True:
            value = cache.get(id, "Item not found")
            await websocket.send_json(value)
            await asyncio.sleep(5)  # Adjust the interval as needed
    except WebSocketDisconnect:
        print(f"Client disconnected")


#returns an entry from cache based on the id
@router.get('/cache/{id}')
def get_cache_value(id: str):
    return cache.get(id, "Item not found")


# adds an entry to the cache. If the ID is already taken, the entry is added to the corresponding list, otherwise a
# new entry is created with the ID. If "extend" in the request is True, the content of value is added to the existing
# list, otherwise the value is added to the entry as a list.
@router.post('/addValueToCache/{id}')
async def add_value_to_cache(id: str, value: apiBaseClasses.Cache):
    if value.extend:
        if id in cache.keys():
            cache[id].extend(value.value)
        else:
            cache[id] = []
            cache[id].extend(value.value)
    else:
        if id in cache.keys():
            cache[id].append(value.value)
        else:
            cache[id] = []
            cache[id].append(value.value)

    return {'msg': f'was loaded into the cache under the id: {id}'}


# remove entry of cache based on id
@router.get("/removeCacheEntry/{id}")
async def clear_cache(id: str):
    if id in cache:
        cache.pop(id)  # Entfernt den Eintrag mit dem Schlüssel id
        return {'msg': f"Entry with id {id} removed"}
    else:
        return {'msg': f"Entry with id {id} not found"}
