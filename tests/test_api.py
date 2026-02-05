from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # check some known activity keys exist
    assert "Basketball" in data


def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    email = "test_student@mergington.edu"

    # ensure email not in participants
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # unregister
    resp_del = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_del.status_code == 200
    assert email not in activities[activity]["participants"]

    # unregistering again should 404
    resp_del2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_del2.status_code == 404


def test_signup_nonexistent_activity():
    resp = client.post("/activities/Nonexistent/signup?email=noone@nowhere.edu")
    assert resp.status_code == 404


def test_unregister_nonexistent_activity():
    resp = client.delete("/activities/Nonexistent/participants?email=noone@nowhere.edu")
    assert resp.status_code == 404
