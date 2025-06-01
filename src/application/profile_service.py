"""Application services for profile operations."""
from typing import List, Optional, Protocol

from src.domain.models.profile import Profile, ProfileSearchResult
from src.domain.validators.profile_validator import ProfileValidator


class ApiClientProtocol(Protocol):
    """Protocol for API clients that can fetch profile data."""
    
    def get_profile(self, username: str) -> Profile:
        """Fetch a single profile by username."""
        ...
    
    def search_profiles(self, query: str) -> ProfileSearchResult:
        """Search for profiles matching the query."""
        ...


class ProfileService:
    """Service for Instagram profile operations."""
    
    def __init__(self, api_client: ApiClientProtocol) -> None:
        """
        Initialize the profile service.
        
        Args:
            api_client: Client for accessing the Instagram API
        """
        self._api_client = api_client
        self._validator = ProfileValidator()
    
    def get_profile(self, username: str) -> tuple[Optional[Profile], Optional[str]]:
        """
        Get a profile by username.
        
        Args:
            username: The Instagram username to look up
            
        Returns:
            A tuple of (profile, error_message)
        """
        is_valid, error = self._validator.validate_username(username)
        if not is_valid:
            return None, error
            
        try:
            profile = self._api_client.get_profile(username)
            return profile, None
        except Exception as e:
            return None, str(e)
    
    def search_profiles(self, query: str) -> tuple[Optional[List[Profile]], Optional[str]]:
        """
        Search for profiles matching the query.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            A tuple of (profiles, error_message)
        """
        if not query:
            return None, "Search query cannot be empty"
            
        try:
            result = self._api_client.search_profiles(query)
            return result.profiles, None
        except Exception as e:
            return None, str(e)