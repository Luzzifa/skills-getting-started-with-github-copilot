"""Tests for the activities endpoints."""
import pytest


def test_get_activities_success(client):
    """Test retrieving all activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify activities is a dict
    assert isinstance(activities, dict)
    
    # Verify expected activities exist
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Squad",
        "Art Workshop",
        "Drama Club",
        "Science Club",
        "Debate Society"
    ]
    for activity_name in expected_activities:
        assert activity_name in activities


def test_get_activities_structure(client):
    """Test that each activity has the correct structure."""
    response = client.get("/activities")
    activities = response.json()
    
    # Check first activity's structure
    first_activity = activities["Chess Club"]
    
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    
    # Verify data types
    assert isinstance(first_activity["description"], str)
    assert isinstance(first_activity["schedule"], str)
    assert isinstance(first_activity["max_participants"], int)
    assert isinstance(first_activity["participants"], list)


def test_get_activities_participants(client):
    """Test that participants list is populated."""
    response = client.get("/activities")
    activities = response.json()
    
    chess_club = activities["Chess Club"]
    
    # Verify there are initial participants
    assert len(chess_club["participants"]) > 0
    
    # Verify participants are email strings
    for participant in chess_club["participants"]:
        assert isinstance(participant, str)
        assert "@" in participant
