"""Pytest configuration and shared fixtures for API tests."""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store the original state
    original_activities = copy.deepcopy(activities)
    
    yield
    
    # Restore the original state after the test
    activities.clear()
    activities.update(original_activities)
