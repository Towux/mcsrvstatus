"""Tests for async mcsrvstatus client."""

import unittest
import asyncio
from unittest.mock import patch, Mock, AsyncMock
import aiohttp
from mcsrvstatus import AsyncMinecraftServerStatus
from mcsrvstatus.exceptions import ServerNotFoundError, APIError, ConnectionError


class TestAsyncMinecraftServerStatus(unittest.TestCase):
    """Tests for AsyncMinecraftServerStatus class."""
    
    def setUp(self):
        """Setup before each test."""
        self.client = AsyncMinecraftServerStatus()
    
    def tearDown(self):
        """Cleanup after each test."""
        asyncio.run(self.client.close())
    
    @patch('mcsrvstatus.async_client.aiohttp.ClientSession.get')
    def test_get_server_status_success(self, mock_get):
        """Test successful server status retrieval."""
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            'online': True,
            'ip': '127.0.0.1',
            'port': 25565,
            'players': {'online': 5, 'max': 20},
            'version': '1.19.4',
            'motd': {'clean': ['Test Server']}
        })
        mock_response.raise_for_status = Mock()
        mock_get.return_value.__aenter__.return_value = mock_response
        
        async def test():
            result = await self.client.get_server_status('test.server.com')
            self.assertTrue(result.online)
            self.assertEqual(result.players.online, 5)
            self.assertEqual(result.version.name, '1.19.4')
        
        asyncio.run(test())
    
    @patch('mcsrvstatus.async_client.aiohttp.ClientSession.get')
    def test_get_server_status_offline(self, mock_get):
        """Test offline server status."""
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'online': False})
        mock_response.raise_for_status = Mock()
        mock_get.return_value.__aenter__.return_value = mock_response
        
        async def test():
            with self.assertRaises(ServerNotFoundError):
                await self.client.get_server_status('offline.server.com')
        
        asyncio.run(test())
    
    @patch('mcsrvstatus.async_client.aiohttp.ClientSession.get')
    def test_connection_error(self, mock_get):
        """Test connection error handling."""
        mock_get.return_value.__aenter__.side_effect = aiohttp.ClientError("Connection failed")
        
        async def test():
            with self.assertRaises(ConnectionError):
                await self.client.get_server_status('unreachable.server.com')
        
        asyncio.run(test())
    
    @patch('mcsrvstatus.async_client.aiohttp.ClientSession.get')
    def test_is_server_online_true(self, mock_get):
        """Test online status check (server online)."""
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'online': True})
        mock_response.raise_for_status = Mock()
        mock_get.return_value.__aenter__.return_value = mock_response
        
        async def test():
            result = await self.client.is_server_online('online.server.com')
            self.assertTrue(result)
        
        asyncio.run(test())
    
    @patch('mcsrvstatus.async_client.aiohttp.ClientSession.get')
    def test_get_player_count(self, mock_get):
        """Test player count retrieval."""
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            'online': True,
            'players': {'online': 15, 'max': 100}
        })
        mock_response.raise_for_status = Mock()
        mock_get.return_value.__aenter__.return_value = mock_response
        
        async def test():
            online, max_players = await self.client.get_player_count('test.server.com')
            self.assertEqual(online, 15)
            self.assertEqual(max_players, 100)
        
        asyncio.run(test())
    
    @patch('mcsrvstatus.async_client.aiohttp.ClientSession.get')
    def test_get_bedrock_status(self, mock_get):
        """Test Bedrock server status."""
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            'online': True,
            'ip': '127.0.0.1',
            'port': 19132,
            'players': {'online': 10, 'max': 50},
            'version': {'name': 'MCPE', 'protocol': 503}
        })
        mock_response.raise_for_status = Mock()
        mock_get.return_value.__aenter__.return_value = mock_response
        
        async def test():
            result = await self.client.get_bedrock_status('bedrock.server.com')
            self.assertTrue(result.online)
            self.assertEqual(result.port, 19132)
            self.assertEqual(result.players.online, 10)
        
        asyncio.run(test())
    
    def test_context_manager(self):
        """Test usage as async context manager."""
        async def test():
            async with AsyncMinecraftServerStatus() as client:
                self.assertIsInstance(client, AsyncMinecraftServerStatus)
        
        asyncio.run(test())
    
    def test_invalid_api_version(self):
        """Test invalid API version."""
        async def test():
            with self.assertRaises(ValueError):
                await self.client.get_server_status('test.server.com', version=5)
        
        asyncio.run(test())


if __name__ == '__main__':
    unittest.main()
