"""Tests for the signup endpoint."""
import pytest


def test_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_increases_participant_count(client):
    """Test that signup increases the participant count."""
    # Get initial count
    activities_response = client.get("/activities")
    initial_participants = len(activities_response.json()["Soccer Team"]["participants"])
    
    # Sign up a new participant
    signup_response = client.post(
        "/activities/Soccer Team/signup",
        params={"email": "newsoccer@mergington.edu"}
    )
    
    assert signup_response.status_code == 200
    
    # Get updated count
    updated_response = client.get("/activities")
    updated_participants = len(updated_response.json()["Soccer Team"]["participants"])
    
    assert updated_participants == initial_participants + 1
    assert "newsoccer@mergington.edu" in updated_response.json()["Soccer Team"]["participants"]


def test_signup_nonexistent_activity(client):
    """Test signup for a non-existent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate(client):
    """Test that duplicate signup returns 400."""
    # Michael is already signed up for Chess Club
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_activities(client):
    """Test that same student can sign up for multiple activities."""
    email = "multistudent@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify in both activities
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_with_special_characters_in_email(client):
    """Test signup with special characters in email (URL encoding)."""
    response = client.post(
        "/activities/Drama Club/signup",
        params={"email": "student+tag@mergington.edu"}
    )
    
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert "student+tag@mergington.edu" in activities["Drama Club"]["participants"]
