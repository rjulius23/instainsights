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
        self._client = hikerapi.Client(token=api_key)
    
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
        response = self._client.user_by_username_v1(username)
        return self._map_profile_response(response)
    
    def search_profiles(self, query: str) -> ProfileSearchResult:
        """
        Search for profiles matching the query.
        
        Args:
            query: The search query, comma separated lsit of users
            limit: Maximum number of results to return
            
        Returns:
            The search results
            
        Raises:
            Exception: If the API request fails
        """
        response = {"users": [], "total_count": 0}
        user_list = query.split(',')
        for user in user_list:
            if not user.strip():
                raise ValueError("Query cannot contain empty usernames")
            response["users"].append(self._client.user_by_username_v1(user.strip()))
            response["total_count"] += 1
        
        profiles = [self._map_profile_response(user) for user in response.get('users', [])]
        
        return ProfileSearchResult(
            profiles=profiles,
            total_count=response.get('total_count', 0),
            query_time_ms=response.get('query_time_ms', 0)
        )
    
    def _map_profile_response(self, stats: Dict[str, Any]) -> Profile:
        """Map API response to domain model."""
        
        statistics = ProfileStatistics(
            followers_count=stats.get('follower_count', 0),
            following_count=stats.get('following_count', 0),
            posts_count=stats.get('media_count', 0),
            last_updated=datetime.fromtimestamp(stats.get('last_updated', 0))
        )
        
        return Profile(
            username=stats.get('username', ''),
            full_name=stats.get('full_name'),
            bio=stats.get('biography'),
            is_verified=stats.get('is_verified', False),
            is_private=stats.get('is_private', False),
            profile_pic_url=stats.get('profile_pic_url'),
            statistics=statistics
        )
