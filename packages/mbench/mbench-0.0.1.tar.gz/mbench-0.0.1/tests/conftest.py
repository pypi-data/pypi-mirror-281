import pytest

def pytest_addoption(parser):
    parser.addini("performance_monitor_enabled", "Enable or disable the performance monitor", default="true")

@pytest.fixture
def performance_monitor_enabled(pytestconfig):
    return pytestconfig.getini("performance_monitor_enabled") == "true"