"""Domain models for Instagram profiles."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class ProfileStatistics:
    """Statistics for an Instagram profile."""
    followers_count: int
    following_count: int
    posts_count: int
    last_updated: datetime


@dataclass(frozen=True)
class EngagementStatistics:
    """Engagement statistics for an Instagram profile."""
    recent_avg_post_likes: int
    recent_avg_post_comments: int
    recent_avg_post_reshares: int
    recent_post_count: int


@dataclass
class Profile:
    """Instagram profile entity."""
    userid: str
    username: str
    full_name: Optional[str]
    bio: Optional[str]
    is_verified: bool
    is_private: bool
    profile_pic_url: Optional[str]
    statistics: ProfileStatistics
    engagement_stats: EngagementStatistics


@dataclass(frozen=True)
class ProfileSearchResult:
    """Result of a profile search operation."""
    profiles: List[Profile]
    total_count: int
    query_time_ms: int
