from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional

from functools import wraps
import uvicorn, socket, httpx
import inspect

import logging
logging.basicConfig(level=logging.ERROR)

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, 'tuns')

class Message(BaseModel):
    handle: str
    content: str
    id: str
    history: Optional[List[Dict[str, str]]] = None

# too dirty
def find_available_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1

import asyncssh, asyncio
async def create_ssh_tunnel(x,y,z='tuns.sh'):
    try:
        async with asyncssh.connect(z,client_keys=[key_path],known_hosts=None) as conn:
            listener = await conn.forward_remote_port(x, 80, 'localhost', y)
            print("✦/✧","tunnel  | open\n")
            await listener.wait_closed()
    except (OSError, asyncssh.Error) as e:
        print("✦/✧",f"tunnel disconnected: {e}")

def register(handles, network, url, mode):
    try:
        with httpx.Client() as client:
            response = client.post(f"{network}/register", json={"handles":handles, "url":url, "mode":mode})
            if response.status_code==200:
                data = (response.json()).get("content")
                for i in data:
                    if i[0]=="new":
                        print(f"✦/✧ {i[0]}     | {network}/{i[1]}")
                    else:
                        print(f"✦/✧ {i[0]} | {network}/{i[1]}")
            else:
                print("✦/✧ failed to register ⚠️")
    except Exception as e:
        print(f"An error occurred: {e}")

class Cycls:
    def __init__(self, url="", network="https://cycls.com", port=find_available_port(8001)):
        import uuid
        self.subdomain = str(uuid.uuid4())[:8]
        self.server = FastAPI()
        self.network = network
        self.port = port
        self.url = url
        self.apps = {}

    def __call__(self, handle):
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return StreamingResponse(await func(*args, **kwargs))
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return StreamingResponse(func(*args, **kwargs))
            wrapper = async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
            self.apps[handle] = wrapper
            return wrapper
        return decorator
    
    async def gateway(self, request: Request):
        data = await request.json()
        handle = data.get('handle')
        if handle in self.apps:
            func = self.apps[handle]
            message = Message(**data)
            return await func(message) if inspect.iscoroutinefunction(func) else func(message)
        return {"error": "Handle not found"}

    def push(self):
        self.server.post("/gateway")(self.gateway)
        @self.server.on_event("startup")
        def startup_event():
            asyncio.create_task(create_ssh_tunnel(f"{self.subdomain}-cycls", self.port))

        self.publish()

        try:
            uvicorn.run(self.server, host="127.0.0.1", port=self.port, log_level="error")
        except KeyboardInterrupt:
            print(f"\n✦/✧ exit    | done")

    def publish(self):
        # prod catch is too dirty
        prod=False
        if self.url != "":
            prod=True

        print(f"✦/✧ port    | {self.port}")
        if prod:
            print("✦/✧",f"production mode | url: {self.url}")
            register(list(self.apps.keys()), self.network, self.url+"/gateway", "prod")
        else:
            self.url = f"http://{self.subdomain}-cycls.tuns.sh"
            print("✦/✧","mode    | development")
            register(list(self.apps.keys()), self.network, self.url+"/gateway", "dev")
        
# poetry publish --build