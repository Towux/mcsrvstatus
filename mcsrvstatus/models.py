"""Data models for mcsrvstat.us API responses."""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class PlayerInfo:
    """Player information model."""
    online: int = 0
    max: int = 0
    list: List[str] = None
    
    def __post_init__(self):
        if self.list is None:
            self.list = []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlayerInfo':
        """Create PlayerInfo from dictionary."""
        return cls(
            online=data.get('online', 0),
            max=data.get('max', 0),
            list=data.get('list', [])
        )


@dataclass
class ServerVersion:
    """Server version information model."""
    name: Optional[str] = None
    protocol: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Any) -> 'ServerVersion':
        """Create ServerVersion from dictionary or string."""
        if isinstance(data, str):
            return cls(name=data)
        elif isinstance(data, dict):
            return cls(
                name=data.get('name'),
                protocol=data.get('protocol')
            )
        return cls()


@dataclass
class ServerMotd:
    """Server MOTD (Message of the Day) model."""
    raw: List[str] = None
    clean: List[str] = None
    html: List[str] = None
    
    def __post_init__(self):
        if self.raw is None:
            self.raw = []
        if self.clean is None:
            self.clean = []
        if self.html is None:
            self.html = []
    
    @property
    def text(self) -> str:
        """Get clean MOTD as single string."""
        return self.clean[0] if self.clean else ""
    
    @classmethod
    def from_dict(cls, data: Any) -> 'ServerMotd':
        """Create ServerMotd from dictionary or string."""
        if isinstance(data, str):
            return cls(clean=[data])
        elif isinstance(data, dict):
            return cls(
                raw=data.get('raw', []),
                clean=data.get('clean', []),
                html=data.get('html', [])
            )
        return cls()


@dataclass
class ServerStatus:
    """Main server status model."""
    online: bool = False
    ip: Optional[str] = None
    port: Optional[int] = None
    hostname: Optional[str] = None
    icon: Optional[str] = None
    software: Optional[str] = None
    map: Optional[str] = None
    gamemode: Optional[str] = None
    players: Optional[PlayerInfo] = None
    version: Optional[ServerVersion] = None
    motd: Optional[ServerMotd] = None
    debug: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.players is None:
            self.players = PlayerInfo()
        if self.version is None:
            self.version = ServerVersion()
        if self.motd is None:
            self.motd = ServerMotd()
    
    @property
    def is_online(self) -> bool:
        """Check if server is online."""
        return self.online
    
    @property
    def player_count(self) -> tuple[int, int]:
        """Get (online, max) player count."""
        return self.players.online, self.players.max
    
    @property
    def player_list(self) -> List[str]:
        """Get list of online players."""
        return self.players.list
    
    @property
    def server_version(self) -> Optional[str]:
        """Get server version name."""
        return self.version.name
    
    @property
    def server_motd(self) -> str:
        """Get server MOTD as string."""
        return self.motd.text
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ServerStatus':
        """Create ServerStatus from API response dictionary."""
        return cls(
            online=data.get('online', False),
            ip=data.get('ip'),
            port=data.get('port'),
            hostname=data.get('hostname'),
            icon=data.get('icon'),
            software=data.get('software'),
            map=data.get('map'),
            gamemode=data.get('gamemode'),
            players=PlayerInfo.from_dict(data.get('players', {})),
            version=ServerVersion.from_dict(data.get('version')),
            motd=ServerMotd.from_dict(data.get('motd')),
            debug=data.get('debug')
        )


@dataclass
class BedrockServerStatus(ServerStatus):
    """Bedrock server status model with additional fields."""
    edition: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BedrockServerStatus':
        """Create BedrockServerStatus from API response dictionary."""
        base_status = ServerStatus.from_dict(data)
        return cls(
            online=base_status.online,
            ip=base_status.ip,
            port=base_status.port,
            hostname=base_status.hostname,
            icon=base_status.icon,
            software=base_status.software,
            map=base_status.map,
            gamemode=base_status.gamemode,
            players=base_status.players,
            version=base_status.version,
            motd=base_status.motd,
            debug=base_status.debug,
            edition=data.get('edition')
        )
