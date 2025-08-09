"""Asynchronous client for mcsrvstat.us API."""

import aiohttp
import asyncio
from typing import Dict, Any, Optional, Tuple
from .exceptions import ServerNotFoundError, APIError, ConnectionError
from .models import ServerStatus, BedrockServerStatus


class AsyncMinecraftServerStatus:
    """Asynchronous client for mcsrvstat.us API."""
    
    BASE_URL = "https://api.mcsrvstat.us"
    
    def __init__(self, timeout: int = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
    
    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers={'User-Agent': 'mcsrvstatus-python/1.0.0'}
            )
    
    async def _make_request(self, endpoint: str) -> Dict[str, Any]:
        await self._ensure_session()
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            raise ConnectionError(f"API connection error: {e}")
        except ValueError as e:
            raise APIError(f"API response parsing error: {e}")
    
    async def get_server_status(self, server_address: str, version: int = 3) -> ServerStatus:
        if version not in [1, 2, 3]:
            raise ValueError("API version must be 1, 2, or 3")
        
        endpoint = f"{version}/{server_address}"
        data = await self._make_request(endpoint)
        
        if not data.get('online', False):
            raise ServerNotFoundError(f"Server {server_address} is offline or not found")
        
        return ServerStatus.from_dict(data)
    
    async def get_bedrock_status(self, server_address: str, version: int = 3) -> BedrockServerStatus:
        if version not in [1, 2, 3]:
            raise ValueError("API version must be 1, 2, or 3")
        
        endpoint = f"bedrock/{version}/{server_address}"
        data = await self._make_request(endpoint)
        
        if not data.get('online', False):
            raise ServerNotFoundError(f"Bedrock server {server_address} is offline or not found")
        
        return BedrockServerStatus.from_dict(data)
    
    async def get_server_icon(self, server_address: str) -> Optional[str]:
        try:
            status = await self.get_server_status(server_address)
            return status.icon
        except (ServerNotFoundError, APIError):
            return None
    
    async def is_server_online(self, server_address: str) -> bool:
        try:
            status = await self.get_server_status(server_address)
            return status.online
        except (ServerNotFoundError, APIError, ConnectionError):
            return False
    
    async def get_player_count(self, server_address: str) -> Tuple[int, int]:
        status = await self.get_server_status(server_address)
        return status.player_count
    
    async def get_server_version(self, server_address: str) -> Optional[str]:
        try:
            status = await self.get_server_status(server_address)
            return status.server_version
        except (ServerNotFoundError, APIError):
            return None
    
    async def get_server_motd(self, server_address: str) -> Optional[str]:
        try:
            status = await self.get_server_status(server_address)
            return status.server_motd
        except (ServerNotFoundError, APIError):
            return None
    
    async def get_player_list(self, server_address: str) -> list:
        try:
            status = await self.get_server_status(server_address)
            return status.player_list
        except (ServerNotFoundError, APIError):
            return []
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
