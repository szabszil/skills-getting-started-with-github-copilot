import copy
from pathlib import Path

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_email():
    original_activities = copy.deepcopy(activities)

    try:
        response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

        assert response.status_code == 200
        assert response.json() == {
            "message": "Removed michael@mergington.edu from Chess Club"
        }
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    finally:
        activities.clear()
        activities.update(original_activities)


def test_signup_handler_refreshes_activities_in_frontend_script():
    app_js = Path("src/static/app.js").read_text()
    signup_handler_start = app_js.index('signupForm.addEventListener("submit"')
    signup_handler_end = app_js.index("// Initialize app", signup_handler_start)
    signup_handler_block = app_js[signup_handler_start:signup_handler_end]

    assert "signupForm.reset();" in signup_handler_block
    assert "await fetchActivities();" in signup_handler_block
