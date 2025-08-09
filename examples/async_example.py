"""Async usage examples for mcsrvstatus library."""

import asyncio
from mcsrvstatus import AsyncMinecraftServerStatus
from mcsrvstatus.exceptions import ServerNotFoundError, APIError


async def async_example():
    """Demonstrate asynchronous client usage."""
    server_address = "mc.hypixel.net"
    
    print(f"Checking server: {server_address}")
    print("-" * 50)
    
    async with AsyncMinecraftServerStatus() as client:
        try:
            is_online = await client.is_server_online(server_address)
            print(f"Server online: {is_online}")
            
            if is_online:
                status = await client.get_server_status(server_address)
                
                print(f"IP: {status.get('ip', 'N/A')}")
                print(f"Port: {status.get('port', 'N/A')}")
                
                online_players, max_players = await client.get_player_count(server_address)
                print(f"Players online: {online_players}/{max_players}")
                
                version = await client.get_server_version(server_address)
                if version:
                    print(f"Version: {version}")
                
                motd = await client.get_server_motd(server_address)
                if motd:
                    print(f"MOTD: {motd}")
        
        except ServerNotFoundError as e:
            print(f"Error: {e}")
        except APIError as e:
            print(f"API Error: {e}")


async def multiple_servers_example():
    """Check multiple servers concurrently."""
    print("\\nMultiple Servers Check:")
    print("-" * 50)
    
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
    """Check a single server."""
    try:
        if await client.is_server_online(server):
            online, max_players = await client.get_player_count(server)
            print(f"{server}: {online}/{max_players} players")
        else:
            print(f"{server}: Offline")
    except Exception as e:
        print(f"{server}: Error - {e}")


async def main():
    """Main async function."""
    await async_example()
    await multiple_servers_example()


if __name__ == "__main__":
    asyncio.run(main())
