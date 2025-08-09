"""Tests for sync mcsrvstatus client."""

import unittest
from unittest.mock import patch, Mock
import requests
from mcsrvstatus import MinecraftServerStatus
from mcsrvstatus.exceptions import ServerNotFoundError, APIError, ConnectionError


class TestMinecraftServerStatus(unittest.TestCase):
    """Tests for MinecraftServerStatus class."""
    
    def setUp(self):
        """Setup before each test."""
        self.client = MinecraftServerStatus()
    
    def tearDown(self):
        """Cleanup after each test."""
        self.client.close()
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_get_server_status_success(self, mock_get):
        """Test successful server status retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'online': True,
            'ip': '127.0.0.1',
            'port': 25565,
            'players': {'online': 5, 'max': 20},
            'version': '1.19.4',
            'motd': {'clean': ['Test Server']}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.get_server_status('test.server.com')
        
        self.assertTrue(result.online)
        self.assertEqual(result.players.online, 5)
        self.assertEqual(result.version.name, '1.19.4')
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_get_server_status_offline(self, mock_get):
        """Test offline server status."""
        mock_response = Mock()
        mock_response.json.return_value = {'online': False}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with self.assertRaises(ServerNotFoundError):
            self.client.get_server_status('offline.server.com')
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_connection_error(self, mock_get):
        """Test connection error handling."""
        mock_get.side_effect = requests.exceptions.RequestException("Connection failed")
        
        with self.assertRaises(ConnectionError):
            self.client.get_server_status('unreachable.server.com')
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_is_server_online_true(self, mock_get):
        """Test online status check (server online)."""
        mock_response = Mock()
        mock_response.json.return_value = {'online': True}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.is_server_online('online.server.com')
        self.assertTrue(result)
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_is_server_online_false(self, mock_get):
        """Test online status check (server offline)."""
        mock_response = Mock()
        mock_response.json.return_value = {'online': False}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.is_server_online('offline.server.com')
        self.assertFalse(result)
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_get_player_count(self, mock_get):
        """Test player count retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'online': True,
            'players': {'online': 15, 'max': 100}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        online, max_players = self.client.get_player_count('test.server.com')
        self.assertEqual(online, 15)
        self.assertEqual(max_players, 100)
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_get_server_version(self, mock_get):
        """Test server version retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'online': True,
            'version': '1.20.1'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        version = self.client.get_server_version('test.server.com')
        self.assertEqual(version, '1.20.1')
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_get_server_motd(self, mock_get):
        """Test server MOTD retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'online': True,
            'motd': {'clean': ['Welcome to our server!']}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        motd = self.client.get_server_motd('test.server.com')
        self.assertEqual(motd, 'Welcome to our server!')
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_get_player_list(self, mock_get):
        """Test player list retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'online': True,
            'players': {
                'online': 3,
                'max': 20,
                'list': ['Player1', 'Player2', 'Player3']
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        players = self.client.get_player_list('test.server.com')
        self.assertEqual(len(players), 3)
        self.assertIn('Player1', players)
        self.assertIn('Player2', players)
    
    def test_context_manager(self):
        """Test usage as context manager."""
        with MinecraftServerStatus() as client:
            self.assertIsInstance(client, MinecraftServerStatus)
    
    def test_invalid_api_version(self):
        """Test invalid API version."""
        with self.assertRaises(ValueError):
            self.client.get_server_status('test.server.com', version=5)
    
    @patch('mcsrvstatus.client.requests.Session.get')
    def test_bedrock_server_status(self, mock_get):
        """Test Bedrock server status retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'online': True,
            'ip': '127.0.0.1',
            'port': 19132,
            'players': {'online': 10, 'max': 50},
            'version': {'name': 'MCPE', 'protocol': 503}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.get_bedrock_status('bedrock.server.com')
        
        self.assertTrue(result.online)
        self.assertEqual(result.port, 19132)
        self.assertEqual(result.players.online, 10)


if __name__ == '__main__':
    unittest.main()
