"""Client for the HikerAPI Instagram API."""
from datetime import datetime
from typing import Dict, Any, List, Optional

import hikerapi

from src.domain.models.profile import Profile, ProfileStatistics, ProfileSearchResult


class HikerApiClient:
    """Client for interacting with the HikerAPI Instagram API."""
    
    def __init__(self, api_key: str) -> None:
        """
        Initialize the HikerAPI client.
        
        Args:
            api_key: The API key for authentication
        """
        self._client = hikerapi.Client()
        self._client.api_key = api_key
    
    def get_profile(self, username: str) -> Profile:
        """
        Fetch a profile by username.
        
        Args:
            username: The Instagram username to look up
            
        Returns:
            The profile data
            
        Raises:
            Exception: If the API request fails
        """
        response = self._client.user_info(username)
        return self._map_profile_response(response)
    
    def search_profiles(self, query: str, limit: int = 10) -> ProfileSearchResult:
        """
        Search for profiles matching the query.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            The search results
            
        Raises:
            Exception: If the API request fails
        """
        response = self._client.search_users(query, limit=limit)
        
        profiles = [self._map_profile_response(user) for user in response.get('users', [])]
        
        return ProfileSearchResult(
            profiles=profiles,
            total_count=response.get('total_count', 0),
            query_time_ms=response.get('query_time_ms', 0)
        )
    
    def _map_profile_response(self, data: Dict[str, Any]) -> Profile:
        """Map API response to domain model."""
        stats = data.get('statistics', {})
        
        statistics = ProfileStatistics(
            followers_count=stats.get('followers_count', 0),
            following_count=stats.get('following_count', 0),
            posts_count=stats.get('posts_count', 0),
            engagement_rate=stats.get('engagement_rate', 0.0),
            avg_likes=stats.get('avg_likes', 0.0),
            avg_comments=stats.get('avg_comments', 0.0),
            last_updated=datetime.fromtimestamp(stats.get('last_updated', 0))
        )
        
        return Profile(
            username=data.get('username', ''),
            full_name=data.get('full_name'),
            bio=data.get('biography'),
            is_verified=data.get('is_verified', False),
            is_private=data.get('is_private', False),
            profile_pic_url=data.get('profile_pic_url'),
            statistics=statistics
        )
