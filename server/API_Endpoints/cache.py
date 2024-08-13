import random
from server.securityCheck import SecurityCheck
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter
import asyncio
from server import apiBaseClasses

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
@router.get('/cache')
def get_cache_value(cache_id: apiBaseClasses.CacheId):
    if SecurityCheck().is_user_token_valid(cache_id.token):
        return cache.get(cache_id, "Item not found")
    return {'msg': "Access denied"}


# Adds an entry to the cache. If the ID is already taken, it adds the entry to the corresponding list.
# Otherwise, it creates a new entry with the ID. If "extend" in the request is True, it adds the content
# of value to the existing list. Otherwise, it adds the value as a list to the entry.

@router.post('/addValueToCache')
async def add_value_to_cache(value: apiBaseClasses.Cache):

    if SecurityCheck().is_user_token_valid(value.token):
        if value.extend:
            if value.cache_id in cache.keys():
                cache[value.cache_id].extend(value.value)
            else:
                cache[value.cache_id] = []
                cache[value.cache_id].extend(value.value)
        else:
            if value.cache_id in cache.keys():
                cache[value.cache_id].append(value.value)
            else:
                cache[value.cache_id] = []
                cache[value.cache_id].append(value.value)

        return {'msg': f'was loaded into the cache under the id: {value.cache_id}'}

    return {'msg': "Access denied"}

# remove entry of cache based on id
@router.get("/removeCacheEntry")
async def clear_cache(cache_id: apiBaseClasses.CacheId):
    if SecurityCheck().is_user_token_valid(cache_id.token):
        if cache_id not in cache.keys():
            return {'msg': f"Entry with id {cache_id} not found"}
        else:
            cache.pop(cache_id)
            return {'msg': f"Entry with id {cache_id} removed"}
    return {'msg': "Access denied"}

# checks whether an id is already occupied
@router.get("/cacheIdIsAssigned")
async def cache_id_is_assigned(cache_id: apiBaseClasses.CacheId):
    if SecurityCheck().is_user_token_valid(cache_id.token):
        if cache_id in cache.keys():
            return True
        else:
            return False
    return {'msg': "Access denied"}


# returns an unused random id from numbers
@router.get('/getUnusedId')
async def get_unused_id(token: apiBaseClasses.Token):

    if SecurityCheck().is_user_token_valid(token.token):
        while True:
            new_id = str(random.randint(999, 9999))

            if new_id not in cache.keys():
                return {'new_id': new_id}

    return {'msg': "Access denied"}