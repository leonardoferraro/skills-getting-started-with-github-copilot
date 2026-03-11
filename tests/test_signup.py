import src.app as app_module


def test_signup_succeeds_for_existing_activity_and_new_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    signup_path = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(signup_path)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_when_activity_does_not_exist(client):
    # Arrange
    signup_path = "/activities/Unknown Club/signup?email=test@mergington.edu"

    # Act
    response = client.post(signup_path)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_when_student_is_already_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = app_module.activities[activity_name]["participants"][0]
    signup_path = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(signup_path)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    max_participants = app_module.activities[activity_name]["max_participants"]
    app_module.activities[activity_name]["participants"] = [
        f"student{index}@mergington.edu" for index in range(max_participants)
    ]
    signup_path = f"/activities/{activity_name}/signup?email=late@mergington.edu"

    # Act
    response = client.post(signup_path)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}
