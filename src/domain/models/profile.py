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
    engagement_rate: float
    avg_likes: float
    avg_comments: float
    last_updated: datetime


@dataclass(frozen=True)
class Profile:
    """Instagram profile entity."""
    username: str
    full_name: Optional[str]
    bio: Optional[str]
    is_verified: bool
    is_private: bool
    profile_pic_url: Optional[str]
    statistics: ProfileStatistics


@dataclass(frozen=True)
class ProfileSearchResult:
    """Result of a profile search operation."""
    profiles: List[Profile]
    total_count: int
    query_time_ms: int
