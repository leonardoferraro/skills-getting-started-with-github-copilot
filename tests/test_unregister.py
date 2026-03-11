import src.app as app_module


def test_unregister_succeeds_for_registered_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = app_module.activities[activity_name]["participants"][0]
    unregister_path = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.delete(unregister_path)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_when_activity_does_not_exist(client):
    # Arrange
    unregister_path = "/activities/Unknown Club/signup?email=test@mergington.edu"

    # Act
    response = client.delete(unregister_path)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_when_student_is_not_registered(client):
    # Arrange
    unregister_path = "/activities/Chess Club/signup?email=missing@mergington.edu"

    # Act
    response = client.delete(unregister_path)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
