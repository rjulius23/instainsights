"""Tests for HikerAPI client."""
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.domain.models.profile import Profile, ProfileStatistics
from src.infrastructure.api.hiker_api_client import HikerApiClient


class TestHikerApiClient:
    """Test suite for HikerApiClient."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a mock hikerapi client
        self.mock_hikerapi = MagicMock()
        
        # Patch the hikerapi.Client to return our mock
        with patch('hikerapi.Client', return_value=self.mock_hikerapi):
            self.api_client = HikerApiClient(api_key="test_key")
    
    def test_get_profile(self):
        """Test fetching a profile by username."""
        # Mock API response
        mock_response = {
            'username': 'testuser',
            'full_name': 'Test User',
            'biography': 'Test bio',
            'is_verified': True,
            'is_private': False,
            'profile_pic_url': 'https://example.com/pic.jpg',
            'follower_count': 1000,
            'following_count': 500,
            'media_count': 100,
            'last_updated': 1672531200  # 2023-01-01 00:00:00
        }
        
        # Configure mock to return our response
        self.mock_hikerapi.user_by_username_v1.return_value = mock_response
        
        # Call the method
        profile = self.api_client.get_profile('testuser')
        
        # Verify the mock was called correctly
        self.mock_hikerapi.user_by_username_v1.assert_called_once_with('testuser')
        
        # Verify the returned profile
        assert isinstance(profile, Profile)
        assert profile.username == 'testuser'
        assert profile.full_name == 'Test User'
        assert profile.bio == 'Test bio'
        assert profile.is_verified is True
        assert profile.is_private is False
        assert profile.profile_pic_url == 'https://example.com/pic.jpg'
        
        # Verify statistics
        stats = profile.statistics
        assert isinstance(stats, ProfileStatistics)
        assert stats.followers_count == 1000
        assert stats.following_count == 500
        assert stats.posts_count == 100
        assert stats.last_updated == datetime.fromtimestamp(1672531200)
    
    def test_search_profiles(self):
        """Test searching for profiles."""
        # Mock API response
        mock_responses = [
            {
                    'username': 'user1',
                    'full_name': 'User One',
                    'biography': 'Bio 1',
                    'is_verified': False,
                    'is_private': False,
                    'profile_pic_url': 'https://example.com/pic1.jpg',
                    'follower_count': 1000,
                    'following_count': 500,
                    'posts_count': 100,
                    'last_updated': 1672531200  # 2023-01-01 00:00:00
            },
            {
                    'username': 'user2',
                    'full_name': 'User Two',
                    'biography': 'Bio 2',
                    'is_verified': True,
                    'is_private': True,
                    'profile_pic_url': 'https://example.com/pic2.jpg',
                    'follower_count': 5000,
                    'following_count': 1000,
                    'posts_count': 200,
                    'last_updated': 1672617600  # 2023-01-02 00:00:00
            }
        ]
        
        # Configure mock to return our response
        self.mock_hikerapi.user_by_username_v1.return_value = mock_responses[0]
        self.mock_hikerapi.user_by_username_v1.side_effect = mock_responses
        
        # Call the method
        result = self.api_client.search_profiles('user1,user2')
        
        # Verify the returned result
        assert self.mock_hikerapi.user_by_username_v1.call_count == 2
        assert len(result.profiles) == 2
        assert result.total_count == 2
        
        # Verify first profile
        profile1 = result.profiles[0]
        assert profile1.username == 'user1'
        assert profile1.full_name == 'User One'
        assert profile1.statistics.followers_count == 1000
        
        # Verify second profile
        profile2 = result.profiles[1]
        assert profile2.username == 'user2'
        assert profile2.full_name == 'User Two'
        assert profile2.statistics.followers_count == 5000
