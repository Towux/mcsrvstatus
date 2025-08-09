"""Synchronous client for mcsrvstat.us API."""

import requests
from typing import Dict, Any, Optional, Tuple
from .exceptions import ServerNotFoundError, APIError, ConnectionError
from .models import ServerStatus, BedrockServerStatus


class MinecraftServerStatus:
    """Synchronous client for mcsrvstat.us API."""
    
    BASE_URL = "https://api.mcsrvstat.us"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'mcsrvstatus-python/1.0.0'
        })
    
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")
        except ValueError as e:
            raise APIError(f"API response parsing error: {e}")
    
    def get_server_status(self, server_address: str, version: int = 3) -> ServerStatus:
        if version not in [1, 2, 3]:
            raise ValueError("API version must be 1, 2, or 3")
        
        endpoint = f"{version}/{server_address}"
        data = self._make_request(endpoint)
        
        if not data.get('online', False):
            raise ServerNotFoundError(f"Server {server_address} is offline or not found")
        
        return ServerStatus.from_dict(data)
    
    def get_bedrock_status(self, server_address: str, version: int = 3) -> BedrockServerStatus:
        if version not in [1, 2, 3]:
            raise ValueError("API version must be 1, 2, or 3")
        
        endpoint = f"bedrock/{version}/{server_address}"
        data = self._make_request(endpoint)
        
        if not data.get('online', False):
            raise ServerNotFoundError(f"Bedrock server {server_address} is offline or not found")
        
        return BedrockServerStatus.from_dict(data)
    
    def get_server_icon(self, server_address: str) -> Optional[str]:
        try:
            status = self.get_server_status(server_address)
            return status.icon
        except (ServerNotFoundError, APIError):
            return None
    
    def is_server_online(self, server_address: str) -> bool:
        try:
            status = self.get_server_status(server_address)
            return status.online
        except (ServerNotFoundError, APIError, ConnectionError):
            return False
    
    def get_player_count(self, server_address: str) -> Tuple[int, int]:
        status = self.get_server_status(server_address)
        return status.player_count
    
    def get_server_version(self, server_address: str) -> Optional[str]:
        try:
            status = self.get_server_status(server_address)
            return status.server_version
        except (ServerNotFoundError, APIError):
            return None
    
    def get_server_motd(self, server_address: str) -> Optional[str]:
        try:
            status = self.get_server_status(server_address)
            return status.server_motd
        except (ServerNotFoundError, APIError):
            return None
    
    def get_player_list(self, server_address: str) -> list:
        try:
            status = self.get_server_status(server_address)
            return status.player_list
        except (ServerNotFoundError, APIError):
            return []
    
    def close(self):
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()