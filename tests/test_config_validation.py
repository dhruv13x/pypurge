import json
import pytest
from pypurge.modules.config import validate_config

def test_validate_config_valid(fs):
    """Test valid configuration passes validation."""
    valid_config = {
        "dir_groups": {"Custom": ["foo"]},
        "file_groups": {"Temp": ["*.tmp"]},
        "exclude_dirs": ["node_modules"],
        "exclude_patterns": ["*.bak"],
    }
    # It should not raise error
    validate_config(valid_config)

def test_validate_config_invalid_type(fs):
    """Test invalid configuration type raises error."""
    invalid_config = {
        "dir_groups": ["should be dict"],
    }
    with pytest.raises(Exception): # We'll refine this to ValidationError later
        validate_config(invalid_config)

def test_validate_config_invalid_structure(fs):
    """Test invalid structure (values not lists of strings)."""
    invalid_config = {
        "dir_groups": {"Custom": "should be list"},
    }
    with pytest.raises(Exception):
        validate_config(invalid_config)
