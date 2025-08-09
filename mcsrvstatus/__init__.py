"""Python library for mcsrvstat.us API - Minecraft server status checker."""

from .client import MinecraftServerStatus
from .async_client import AsyncMinecraftServerStatus
from .exceptions import (
    MCSrvStatError,
    ServerNotFoundError,
    APIError,
    ConnectionError
)
from .models import (
    ServerStatus,
    BedrockServerStatus,
    PlayerInfo,
    ServerVersion,
    ServerMotd
)

__version__ = "1.0.5"
__author__ = "Towux"
__description__ = "Python library for mcsrvstat.us API"

__all__ = [
    "MinecraftServerStatus",
    "AsyncMinecraftServerStatus",
    "MCSrvStatError", 
    "ServerNotFoundError",
    "APIError",
    "ConnectionError",
    "ServerStatus",
    "BedrockServerStatus",
    "PlayerInfo",
    "ServerVersion",
    "ServerMotd"
]
