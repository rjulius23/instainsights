"""Validators for profile-related operations."""
import re
from typing import Optional, Tuple


class ProfileValidator:
    """Validator for Instagram profile operations."""
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, Optional[str]]:
        """
        Validate an Instagram username.
        
        Args:
            username: The username to validate
            
        Returns:
            A tuple of (is_valid, error_message)
        """
        if not username:
            return False, "Username cannot be empty"
            
        # Instagram usernames can contain letters, numbers, periods and underscores
        # They cannot start with a period and are limited to 30 characters
        pattern = r'^[a-zA-Z0-9_][a-zA-Z0-9_.]{0,29}$'
        
        if not re.match(pattern, username):
            return False, "Invalid username format"
            
        return True, None
