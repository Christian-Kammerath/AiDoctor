import random

from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
import asyncio
import apiBaseClasses

router = APIRouter()

cache = {}


# can use Websocket to return continuously changing data from cache.
@router.websocket("/cache/socket/{cache_id}")
async def websocket_endpoint(websocket: WebSocket, cache_id: str):
    await websocket.accept()
    try:
        while True:
            value = cache.get(cache_id, "Item not found")
            await websocket.send_json(value)
            await asyncio.sleep(5)  # Adjust the interval as needed
    except WebSocketDisconnect:
        print(f"Client disconnected")


# returns an entry from cache based on the id
@router.get('/cache/{cache_id}')
def get_cache_value(cache_id: str):
    return cache.get(cache_id, "Item not found")


# Adds an entry to the cache. If the ID is already taken, it adds the entry to the corresponding list.
# Otherwise, it creates a new entry with the ID. If "extend" in the request is True, it adds the content
# of value to the existing list. Otherwise, it adds the value as a list to the entry.

@router.post('/addValueToCache/{cache_id}')
async def add_value_to_cache(cache_id: str, value: apiBaseClasses.Cache):
    if value.extend:
        if cache_id in cache.keys():
            cache[cache_id].extend(value.value)
        else:
            cache[cache_id] = []
            cache[cache_id].extend(value.value)
    else:
        if cache_id in cache.keys():
            cache[cache_id].append(value.value)
        else:
            cache[cache_id] = []
            cache[cache_id].append(value.value)

    return {'msg': f'was loaded into the cache under the id: {cache_id}'}


# remove entry of cache based on id
@router.get("/removeCacheEntry/{cache_id}")
async def clear_cache(cache_id: str):
    if cache_id not in cache.keys():
        return {'msg': f"Entry with id {cache_id} not found"}
    else:
        cache.pop(cache_id)
        return {'msg': f"Entry with id {cache_id} removed"}


# checks whether an id is already occupied
@router.get("/cacheIdIsAssigned/{cache_id}")
async def cache_id_is_assigned(cache_id: str):
    if cache_id in cache.keys():
        return True
    else:
        return False


# returns an unused random id from numbers
@router.get('/getUnusedId')
async def get_unused_id():
    while True:
        new_id = str(random.randint(999, 9999))

        if new_id not in cache.keys():
            return {'new_id': new_id}
