"""Client for the HikerAPI Instagram API."""
from datetime import datetime
from typing import Dict, Any, List, Optional

import hikerapi

from src.domain.models.profile import EngagementStatistics, Profile, ProfileStatistics, ProfileSearchResult


class HikerApiClient:
    """Client for interacting with the HikerAPI Instagram API."""
    
    def __init__(self, api_key: str) -> None:
        """
        Initialize the HikerAPI client.
        
        Args:
            api_key: The API key for authentication
        """
        self._client = hikerapi.Client(token=api_key)

    def get_engagement_stats(self, userid: str) -> Dict[str, Any]:
        """
        Fetch engagement statistics for a profile by username.
        
        Args:
            id: The Instagram id to look up
            
        Returns:
            Engagement statistics as a dictionary
            
        Raises:
            Exception: If the API request fails
        """
        response = self._client.user_medias_v2(userid)
        result = {}
        top_5_posts_avg_likes = 0
        post_count = 0
        response = response.get('response', {})
        for ix, post in enumerate(response.get('items', [])):
            if 'like_count' in post:
                top_5_posts_avg_likes += post['like_count']
                post_count += 1
            if ix == 4:
                break
        if post_count > 0:
            top_5_posts_avg_likes /= post_count
        result['top_5_posts_avg_likes'] = top_5_posts_avg_likes

        top_5_posts_avg_comments = 0
        for ix, post in enumerate(response.get('items', [])):
            if 'comment_count' in post:
                top_5_posts_avg_comments += post['comment_count']
            if ix == 4:
                break
        if post_count > 0:
            top_5_posts_avg_comments /= post_count
        result['top_5_posts_avg_comments'] = top_5_posts_avg_comments

        top_5_posts_avg_reshares = 0
        for ix, post in enumerate(response.get('items', [])):
            if 'reshare_count' in post:
                top_5_posts_avg_reshares += post['reshare_count']
            if ix == 4:
                break
        if post_count > 0:
            top_5_posts_avg_reshares /= post_count
        result['top_5_posts_avg_reshares'] = top_5_posts_avg_reshares

        result['recent_post_count'] = post_count

        eng_stats = EngagementStatistics(
            recent_avg_post_likes=int(result.get('top_5_posts_avg_likes', 0)),
            recent_avg_post_comments=int(result.get('top_5_posts_avg_comments', 0)),
            recent_avg_post_reshares=int(result.get('top_5_posts_avg_reshares', 0)),
            recent_post_count=int(result.get('recent_post_count', 0))
        )
        
        return eng_stats
    
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
        engagement_stats = self.get_engagement_stats(response.get('pk', ''))
        mapped_response = self._map_profile_response(stats=response, engagement_stats=engagement_stats)
        return mapped_response
    
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
        
        profiles = []
        for user in response.get('users', []):
            engagement_stats = self.get_engagement_stats(user.get('pk', ''))
            profiles.append(self._map_profile_response(stats=user, engagement_stats=engagement_stats))
        
        return ProfileSearchResult(
            profiles=profiles,
            total_count=response.get('total_count', 0),
            query_time_ms=response.get('query_time_ms', 0)
        )
    
    def _map_profile_response(self, stats: Dict[str, Any], engagement_stats: Dict[str, Any]) -> Profile:
        """Map API response to domain model."""
        
        statistics = ProfileStatistics(
            followers_count=stats.get('follower_count', 0),
            following_count=stats.get('following_count', 0),
            posts_count=stats.get('media_count', 0),
            last_updated=datetime.fromtimestamp(stats.get('last_updated', 0))
        )
        
        return Profile(
            userid=stats.get('pk', ''),
            username=stats.get('username', ''),
            full_name=stats.get('full_name'),
            bio=stats.get('biography'),
            is_verified=stats.get('is_verified', False),
            is_private=stats.get('is_private', False),
            profile_pic_url=stats.get('profile_pic_url'),
            statistics=statistics,
            engagement_stats=engagement_stats
        )
