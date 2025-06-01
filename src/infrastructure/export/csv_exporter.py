"""CSV export functionality."""
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.domain.models.profile import Profile


class CsvExporter:
    """Exports profile data to CSV format."""
    
    def export_profiles(self, profiles: List[Profile], filepath: str) -> None:
        """
        Export profiles to a CSV file.
        
        Args:
            profiles: List of profiles to export
            filepath: Path to save the CSV file
            
        Raises:
            IOError: If the file cannot be written
        """
        if not profiles:
            raise ValueError("No profiles to export")
            
        fieldnames = [
            'username', 'full_name', 'is_verified', 'is_private',
            'followers_count', 'following_count',
            'avg_post_likes','avg_post_comments', 'avg_post_reshares', 'posts_count',
            'last_updated'
        ]
        
        rows = []
        for profile in profiles:
            rows.append({
                'username': profile.username,
                'full_name': profile.full_name or '',
                'is_verified': profile.is_verified,
                'is_private': profile.is_private,
                'followers_count': profile.statistics.followers_count,
                'following_count': profile.statistics.following_count,
                'avg_post_likes': profile.engagement_stats.recent_avg_post_likes,
                'avg_post_comments': profile.engagement_stats.recent_avg_post_comments,
                'avg_post_reshares': profile.engagement_stats.recent_avg_post_reshares,
                'recent_posts_count': profile.engagement_stats.recent_post_count,
                'last_updated': profile.statistics.last_updated.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
