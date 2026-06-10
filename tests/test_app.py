from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activities = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200

    activities = response.json()
    assert expected_activities.issubset(set(activities.keys()))

    chess_activity = activities["Chess Club"]
    assert chess_activity["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(chess_activity["participants"], list)


def test_signup_for_activity_adds_participant():
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    response = client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_duplicate_is_rejected():
    # Arrange
    email = "duplicate@student.edu"
    activity_name = "Gym Class"

    # Act
    first_response = client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup",
        params={"email": email},
    )
    duplicate_response = client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup",
        params={"email": email},
    )

    # Assert
    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student is already signed up for this activity"
