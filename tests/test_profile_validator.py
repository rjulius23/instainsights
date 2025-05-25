"""Tests for profile validators."""
import pytest

from src.domain.validators.profile_validator import ProfileValidator


class TestProfileValidator:
    """Test suite for ProfileValidator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = ProfileValidator()
    
    def test_valid_username(self):
        """Test validation of valid usernames."""
        valid_usernames = [
            "user123",
            "john_doe",
            "instagram",
            "user.name",
            "a" * 30  # Max length
        ]
        
        for username in valid_usernames:
            is_valid, error = self.validator.validate_username(username)
            assert is_valid is True
            assert error is None
    
    def test_invalid_username(self):
        """Test validation of invalid usernames."""
        invalid_usernames = [
            "",  # Empty
            ".starts_with_dot",  # Cannot start with dot
            "a" * 31,  # Too long
            "user@name",  # Invalid character
            "user name",  # Space not allowed
            "user-name",  # Hyphen not allowed
        ]
        
        for username in invalid_usernames:
            is_valid, error = self.validator.validate_username(username)
            assert is_valid is False
            assert error is not None
