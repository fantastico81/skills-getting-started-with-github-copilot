import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = {name: {
        "description": details["description"],
        "schedule": details["schedule"],
        "max_participants": details["max_participants"],
        "participants": list(details["participants"]),
    } for name, details in activities.items()}

    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"],
        },
    })

    yield

    activities.clear()
    activities.update(original)


@pytest.fixture()
def client():
    return TestClient(app)


def test_unregister_removes_participant(client):
    response = client.post(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


def test_unregister_returns_404_for_unknown_participant(client):
    response = client.post(
        "/activities/Chess Club/unregister?email=missing@mergington.edu"
    )

    assert response.status_code == 404
