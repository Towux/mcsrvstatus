"""Example showing the new model-based API usage."""

from mcsrvstatus import MinecraftServerStatus, ServerStatus
from mcsrvstatus.exceptions import ServerNotFoundError


def demonstrate_models():
    """Show how to use the new model classes."""
    
    with MinecraftServerStatus() as client:
        try:
            # Get server status using new models
            status = client.get_server_status("mc.hypixel.net")
            
            print("=== Server Information ===")
            print(f"Server: {status.ip}:{status.port}")
            print(f"Online: {status.online}")
            print(f"Hostname: {status.hostname}")
            
            print("\\n=== Player Information ===")
            print(f"Players: {status.players.online}/{status.players.max}")
            if status.players.list:
                print(f"Player list: {', '.join(status.players.list[:3])}...")
            
            print("\\n=== Server Details ===")
            print(f"Version: {status.version.name}")
            if status.version.protocol:
                print(f"Protocol: {status.version.protocol}")
            
            print(f"MOTD: {status.motd.text}")
            if status.motd.clean:
                print(f"Clean MOTD lines: {len(status.motd.clean)}")
            
            if status.software:
                print(f"Software: {status.software}")
            if status.map:
                print(f"Map: {status.map}")
            if status.gamemode:
                print(f"Gamemode: {status.gamemode}")
            
            print("\\n=== Icon ===")
            print(f"Has icon: {'Yes' if status.icon else 'No'}")
            
            # Use convenience properties
            print("\\n=== Convenience Properties ===")
            print(f"Is online: {status.is_online}")
            online, max_players = status.player_count
            print(f"Player count tuple: ({online}, {max_players})")
            print(f"Player list: {status.player_list}")
            print(f"Server version: {status.server_version}")
            print(f"Server MOTD: {status.server_motd}")
            
        except ServerNotFoundError as e:
            print(f"Server error: {e}")
        except Exception as e:
            print(f"Error: {e}")


def compare_old_vs_new():
    """Compare old dictionary access vs new model access."""
    
    with MinecraftServerStatus() as client:
        try:
            status = client.get_server_status("mc.hypixel.net")
            
            print("=== Old Style (still works with helper methods) ===")
            online, max_players = client.get_player_count("mc.hypixel.net")
            version = client.get_server_version("mc.hypixel.net")
            motd = client.get_server_motd("mc.hypixel.net")
            
            print(f"Players: {online}/{max_players}")
            print(f"Version: {version}")
            print(f"MOTD: {motd}")
            
            print("\\n=== New Style (direct model access) ===")
            print(f"Players: {status.players.online}/{status.players.max}")
            print(f"Version: {status.version.name}")
            print(f"MOTD: {status.motd.text}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Model Usage Example")
    print("=" * 50)
    
    demonstrate_models()
    
    print("\\n" + "=" * 50)
    compare_old_vs_new()
