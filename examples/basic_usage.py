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
                
                print(f"IP: {status.get('ip', 'N/A')}")
                print(f"Port: {status.get('port', 'N/A')}")
                
                # Player information
                online_players, max_players = client.get_player_count(server_address)
                print(f"Players online: {online_players}/{max_players}")
                
                # Server version
                version = client.get_server_version(server_address)
                if version:
                    print(f"Version: {version}")
                
                # Server MOTD
                motd = client.get_server_motd(server_address)
                if motd:
                    print(f"MOTD: {motd}")
                
                # Player list (if available)
                players = client.get_player_list(server_address)
                if players:
                    print(f"Players: {', '.join(players[:5])}{'...' if len(players) > 5 else ''}")
                
                # Check for server icon
                icon = client.get_server_icon(server_address)
                if icon:
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
            print(f"Online: {status.get('online', False)}")
            print(f"Players: {status.get('players', {}).get('online', 0)}/{status.get('players', {}).get('max', 0)}")
            
        except ServerNotFoundError:
            print("Bedrock server is offline")
        except Exception as e:
            print(f"Error checking Bedrock server: {e}")


if __name__ == "__main__":
    sync_example()
    bedrock_example()