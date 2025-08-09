"""Basic usage examples for mcsrvstatus library."""

from mcsrvstatus import MinecraftServerStatus
from mcsrvstatus.exceptions import ServerNotFoundError, APIError


def sync_example():
    """Demonstrate synchronous client usage."""
    server_address = "mc.hypixel.net"
    
    print(f"Checking server: {server_address}")
    print("-" * 50)
    
    with MinecraftServerStatus() as client:
        try:
            # Check if server is online
            is_online = client.is_server_online(server_address)
            print(f"Server online: {is_online}")
            
            if is_online:
                # Get full server information
                status = client.get_server_status(server_address)
                
                print(f"IP: {status.ip or 'N/A'}")
                print(f"Port: {status.port or 'N/A'}")
                
                # Player information
                print(f"Players online: {status.players.online}/{status.players.max}")
                
                # Server version
                if status.version.name:
                    print(f"Version: {status.version.name}")
                
                # Server MOTD
                if status.motd.text:
                    print(f"MOTD: {status.motd.text}")
                
                # Player list (if available)
                if status.players.list:
                    players_text = ', '.join(status.players.list[:5])
                    if len(status.players.list) > 5:
                        players_text += "..."
                    print(f"Players: {players_text}")
                
                # Check for server icon
                if status.icon:
                    print("Server icon: Available")
        
        except ServerNotFoundError as e:
            print(f"Error: {e}")
        except APIError as e:
            print(f"API Error: {e}")
        except Exception as e:
            print(f"Unknown error: {e}")


def bedrock_example():
    """Example with Bedrock server."""
    print("\\nBedrock Server Example:")
    print("-" * 50)
    
    with MinecraftServerStatus() as client:
        try:
            bedrock_server = "play.nethergames.org"
            
            status = client.get_bedrock_status(bedrock_server)
            
            print(f"Bedrock server: {bedrock_server}")
            print(f"Online: {status.online}")
            print(f"Players: {status.players.online}/{status.players.max}")
            
        except ServerNotFoundError:
            print("Bedrock server is offline")
        except Exception as e:
            print(f"Error checking Bedrock server: {e}")


if __name__ == "__main__":
    sync_example()
    bedrock_example()