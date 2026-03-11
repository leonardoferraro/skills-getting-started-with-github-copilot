from copy import deepcopy

from fastapi.testclient import TestClient
import pytest

import src.app as app_module


INITIAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    app_module.activities = deepcopy(INITIAL_ACTIVITIES)
    yield
    app_module.activities = deepcopy(INITIAL_ACTIVITIES)
