"""Tests for the unregister endpoint."""
import pytest


def test_unregister_success(client):
    """Test successful unregister from an activity."""
    # Michael is already signed up for Chess Club
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_decreases_participant_count(client):
    """Test that unregister decreases the participant count."""
    # Get initial count
    activities = client.get("/activities").json()
    initial_participants = len(activities["Programming Class"]["participants"])
    
    # Unregister Emma
    unregister_response = client.delete(
        "/activities/Programming Class/unregister",
        params={"email": "emma@mergington.edu"}
    )
    
    assert unregister_response.status_code == 200
    
    # Get updated count
    updated_activities = client.get("/activities").json()
    updated_participants = len(updated_activities["Programming Class"]["participants"])
    
    assert updated_participants == initial_participants - 1
    assert "emma@mergington.edu" not in updated_activities["Programming Class"]["participants"]


def test_unregister_nonexistent_activity(client):
    """Test unregister from a non-existent activity returns 404."""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_not_signed_up(client):
    """Test that unregistering a non-participant returns 400."""
    response = client.delete(
        "/activities/Debate Society/unregister",
        params={"email": "notstudent@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]


def test_unregister_and_signup_again(client):
    """Test that student can unregister and sign up again."""
    email = "flexible@mergington.edu"
    activity = "Art Workshop"
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Sign up again
    signup_again_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_again_response.status_code == 200
    
    # Verify signed up
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_unregister_existing_participant(client):
    """Test unregistering an existing participant works."""
    # John is already in Gym Class
    activities = client.get("/activities").json()
    assert "john@mergington.edu" in activities["Gym Class"]["participants"]
    
    response = client.delete(
        "/activities/Gym Class/unregister",
        params={"email": "john@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify removed
    updated_activities = client.get("/activities").json()
    assert "john@mergington.edu" not in updated_activities["Gym Class"]["participants"]


def test_unregister_with_special_characters_in_email(client):
    """Test unregister with special characters in email (URL encoding)."""
    email = "student+special@mergington.edu"
    
    # Sign up first
    client.post(
        "/activities/Science Club/signup",
        params={"email": email}
    )
    
    # Unregister
    response = client.delete(
        "/activities/Science Club/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify removed
    activities = client.get("/activities").json()
    assert email not in activities["Science Club"]["participants"]
