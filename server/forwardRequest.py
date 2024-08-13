import httpx
import aiofiles
import uuid
import os
from fastapi import BackgroundTasks
from starlette.responses import FileResponse

# Class for forwarding requests. The method GET, POST, the URL and optionally a body must be specified. If request is
# called, the response is returned directly. Alternatively, if file_response is used, request is called in the
# function, temporarily stored and returned as a FileResponse.
class ForwardRequest:
    def __init__(self, method: str, url: str, body: dict = None):
        self.method = method.upper()
        self.url = url
        self.body = body or {}

    async def request(self):
        async with httpx.AsyncClient() as client:
            try:
                if self.method == 'POST':
                    response = await client.post(self.url, json=self.body)
                elif self.method == 'GET':
                    response = await client.get(self.url, params=self.body)
                else:
                    raise ValueError(f"Unsupported method: {self.method}")

                response.raise_for_status()  # Raises an error for bad responses
                return response

            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                return None
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

    async def file_response(self, background_tasks: BackgroundTasks):

        response = await self.request()

        if response is None:
            raise ValueError("No response available. Make sure to call `request` before `file_response`.")

        response = response
        filename = str(uuid.uuid4())

        async with aiofiles.open(f'server/tmp/{filename}', 'wb') as f:
            await f.write(response.content)  # Ensure to use response.content

        background_tasks.add_task(os.remove, f'server/tmp/{filename}')

        return FileResponse(f'server/tmp/{filename}', media_type=response.headers.get('Content-Type'))
