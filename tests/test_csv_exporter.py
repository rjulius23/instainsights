"""Tests for CSV exporter."""
import csv
import os
from datetime import datetime
from tempfile import NamedTemporaryFile

import pytest

from src.domain.models.profile import Profile, ProfileStatistics
from src.infrastructure.export.csv_exporter import CsvExporter


class TestCsvExporter:
    """Test suite for CsvExporter."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.exporter = CsvExporter()
        
        # Create sample profiles for testing
        stats1 = ProfileStatistics(
            followers_count=1000,
            following_count=500,
            posts_count=100,
            engagement_rate=3.5,
            avg_likes=50.0,
            avg_comments=5.0,
            last_updated=datetime(2023, 1, 1, 12, 0, 0)
        )
        
        stats2 = ProfileStatistics(
            followers_count=5000,
            following_count=1000,
            posts_count=200,
            engagement_rate=4.2,
            avg_likes=120.0,
            avg_comments=10.0,
            last_updated=datetime(2023, 1, 2, 12, 0, 0)
        )
        
        self.profile1 = Profile(
            username="user1",
            full_name="User One",
            bio="Bio for user 1",
            is_verified=False,
            is_private=False,
            profile_pic_url="https://example.com/pic1.jpg",
            statistics=stats1
        )
        
        self.profile2 = Profile(
            username="user2",
            full_name="User Two",
            bio="Bio for user 2",
            is_verified=True,
            is_private=True,
            profile_pic_url="https://example.com/pic2.jpg",
            statistics=stats2
        )
        
        self.profiles = [self.profile1, self.profile2]
    
    def test_export_profiles(self):
        """Test exporting profiles to CSV."""
        with NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            filepath = temp_file.name
        
        try:
            # Export profiles
            self.exporter.export_profiles(self.profiles, filepath)
            
            # Verify file exists
            assert os.path.exists(filepath)
            
            # Read and verify contents
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                assert len(rows) == 2
                
                # Check first profile
                assert rows[0]['username'] == 'user1'
                assert rows[0]['full_name'] == 'User One'
                assert rows[0]['is_verified'] == 'False'
                assert rows[0]['is_private'] == 'False'
                assert rows[0]['followers_count'] == '1000'
                assert rows[0]['following_count'] == '500'
                assert rows[0]['posts_count'] == '100'
                assert rows[0]['engagement_rate'] == '3.5'
                assert rows[0]['avg_likes'] == '50.0'
                assert rows[0]['avg_comments'] == '5.0'
                assert rows[0]['last_updated'] == '2023-01-01 12:00:00'
                
                # Check second profile
                assert rows[1]['username'] == 'user2'
                assert rows[1]['full_name'] == 'User Two'
                assert rows[1]['is_verified'] == 'True'
                assert rows[1]['is_private'] == 'True'
                assert rows[1]['followers_count'] == '5000'
                assert rows[1]['following_count'] == '1000'
                assert rows[1]['posts_count'] == '200'
                assert rows[1]['engagement_rate'] == '4.2'
                assert rows[1]['avg_likes'] == '120.0'
                assert rows[1]['avg_comments'] == '10.0'
                assert rows[1]['last_updated'] == '2023-01-02 12:00:00'
                
        finally:
            # Clean up
            if os.path.exists(filepath):
                os.unlink(filepath)
    
    def test_export_empty_profiles(self):
        """Test exporting empty profile list."""
        with NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            filepath = temp_file.name
        
        try:
            # Should raise ValueError
            with pytest.raises(ValueError):
                self.exporter.export_profiles([], filepath)
                
        finally:
            # Clean up
            if os.path.exists(filepath):
                os.unlink(filepath)
