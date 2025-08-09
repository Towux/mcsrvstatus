# mcsrvstatus

![supported python versions](https://img.shields.io/pypi/pyversions/mcsrvstatus.svg) [![current PyPI version](https://img.shields.io/pypi/v/mcsrvstatus.svg)](https://pypi.org/project/mcsrvstatus/) ![GitHub Repo stars](https://img.shields.io/github/stars/Towux/mcsrvstatus)

A Python library for interacting with the mcsrvstat.us API to check Minecraft server status.

## Features

- Check Java and Bedrock Minecraft server status
- Get player count, server version, and MOTD
- Retrieve server icons
- Both synchronous and asynchronous support
- Simple and intuitive API
- Comprehensive error handling

## Installation

```bash
pip install mcsrvstatus
```

## Quick Start

### Synchronous Usage

```python
from mcsrvstatus import MinecraftServerStatus

client = MinecraftServerStatus()

# Check if server is online
is_online = client.is_server_online("mc.hypixel.net")
print(f"Server online: {is_online}")

# Get full server status
status = client.get_server_status("mc.hypixel.net")
print(f"Players: {status.players.online}/{status.players.max}")

client.close()
```

### Asynchronous Usage

```python
import asyncio
from mcsrvstatus import AsyncMinecraftServerStatus

async def main():
    async with AsyncMinecraftServerStatus() as client:
        is_online = await client.is_server_online("mc.hypixel.net")
        print(f"Server online: {is_online}")
        
        status = await client.get_server_status("mc.hypixel.net")
        print(f"Players: {status.players.online}/{status.players.max}")

asyncio.run(main())
```

## API Reference

### MinecraftServerStatus (Sync)

#### Methods

**`get_server_status(server_address: str, version: int = 3) -> Dict[str, Any]`**

Get full server status information.

```python
status = client.get_server_status("play.example.com")
print(f"Online: {status.online}")
print(f"IP: {status.ip}:{status.port}")
print(f"Players: {status.players.online}/{status.players.max}")
print(f"Version: {status.version.name}")
print(f"MOTD: {status.motd.text}")
print(f"Player list: {status.players.list}")
```

**`get_bedrock_status(server_address: str, version: int = 3) -> Dict[str, Any]`**

Get Bedrock server status.

```python
status = client.get_bedrock_status("play.example.com")
```

**`is_server_online(server_address: str) -> bool`**

Check if server is online.

```python
online = client.is_server_online("play.example.com")
```

**`get_player_count(server_address: str) -> Tuple[int, int]`**

Get current and maximum player count.

```python
online_players, max_players = client.get_player_count("play.example.com")
```

**`get_server_version(server_address: str) -> Optional[str]`**

Get server version.

```python
version = client.get_server_version("play.example.com")
```

**`get_server_motd(server_address: str) -> Optional[str]`**

Get server message of the day.

```python
motd = client.get_server_motd("play.example.com")
```

**`get_player_list(server_address: str) -> List[str]`**

Get list of online players (if available).

```python
players = client.get_player_list("play.example.com")
```

**`get_server_icon(server_address: str) -> Optional[str]`**

Get server icon as base64 string.

```python
icon = client.get_server_icon("play.example.com")
```

### AsyncMinecraftServerStatus (Async)

All methods are the same as the sync version but with `async`/`await`:

```python
async with AsyncMinecraftServerStatus() as client:
    status = await client.get_server_status("play.example.com")
    online = await client.is_server_online("play.example.com")
    players = await client.get_player_count("play.example.com")
```

## Error Handling

The library raises specific exceptions for different error cases:

```python
from mcsrvstatus.exceptions import ServerNotFoundError, APIError, ConnectionError

try:
    status = client.get_server_status("nonexistent.server.com")
except ServerNotFoundError:
    print("Server is offline or doesn't exist")
except APIError as e:
    print(f"API error: {e}")
except ConnectionError as e:
    print(f"Network error: {e}")
```

## Examples

### Basic Server Information

```python
from mcsrvstatus import MinecraftServerStatus

client = MinecraftServerStatus()

server = "mc.hypixel.net"

try:
    # Basic info
    print(f"Checking {server}...")
    
    if client.is_server_online(server):
        status = client.get_server_status(server)
        print(f"✓ Online: {status.players.online}/{status.players.max} players")
        print(f"✓ Version: {status.version.name}")
        print(f"✓ MOTD: {status.motd.text}")
    else:
        print("✗ Server is offline")

finally:
    client.close()
```

### Multiple Servers Check

```python
import asyncio
from mcsrvstatus import AsyncMinecraftServerStatus

async def check_servers():
    servers = [
        "mc.hypixel.net",
        "play.mineplex.com", 
        "hub.mcs.gg"
    ]
    
    async with AsyncMinecraftServerStatus() as client:
        tasks = []
        for server in servers:
            task = asyncio.create_task(check_single_server(client, server))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

async def check_single_server(client, server):
    try:
        if await client.is_server_online(server):
            status = await client.get_server_status(server)
            print(f"{server}: {status.players.online}/{status.players.max} players")
        else:
            print(f"{server}: Offline")
    except Exception as e:
        print(f"{server}: Error - {e}")

asyncio.run(check_servers())
```

### Bedrock Server

```python
from mcsrvstatus import MinecraftServerStatus

client = MinecraftServerStatus()

try:
    status = client.get_bedrock_status("play.nethergames.org")
    print(f"Bedrock server online: {status.online}")
    print(f"Players: {status.players.online}/{status.players.max}")
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
```

### Context Manager Usage

```python
from mcsrvstatus import MinecraftServerStatus

# Automatically handles connection cleanup
with MinecraftServerStatus() as client:
    status = client.get_server_status("play.example.com")
    print(f"Server: {status.ip}:{status.port}")
```

## API Versions

The mcsrvstat.us API supports versions 1, 2, and 3 (default). You can specify the version:

```python
# Use API version 2
status = client.get_server_status("play.example.com", version=2)
```

## Requirements

- Python 3.6+
- requests (for sync client)
- aiohttp (for async client)

## License

MIT License - see LICENSE file for details.