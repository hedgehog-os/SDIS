import pytest
from datetime import datetime, timedelta
from persons.Observer import Observer

@pytest.fixture
def observer():
    now = datetime.now()
    logs = {
        "resource_a": now - timedelta(minutes=10),
        "resource_b": now - timedelta(hours=2),
        "resource_c": now - timedelta(minutes=30)
    }
    return Observer(
        observer_id=1,
        fullname="Error Watcher",
        email="error@lab.com",
        access_logs=logs,
        last_accessed=now - timedelta(minutes=10)
    )
def test_log_access_updates_logs_and_timestamp(observer):
    observer.log_access("resource_d")
    assert "resource_d" in observer.access_logs
    assert observer.last_accessed >= datetime.now() - timedelta(seconds=1)

def test_remove_access_log_existing(observer):
    observer.remove_access_log("resource_b")
    assert "resource_b" not in observer.access_logs

def test_remove_access_log_missing(observer):
    observer.remove_access_log("resource_x")  # не должно вызвать ошибку
    assert "resource_x" not in observer.access_logs

def test_get_accessed_resources(observer):
    resources = observer.get_accessed_resources()
    assert set(resources) == {"resource_a", "resource_b", "resource_c"}

def test_get_last_access_time_existing(observer):
    time = observer.get_last_access_time("resource_a")
    assert isinstance(time, datetime)

def test_get_last_access_time_missing(observer):
    assert observer.get_last_access_time("resource_x") is None

def test_was_active_recently_true(observer):
    assert observer.was_active_recently(minutes=15) is True

def test_was_active_recently_false(observer):
    assert observer.was_active_recently(minutes=5) is False

def test_summarize_output(observer):
    summary = observer.summarize()
    assert f"Наблюдатель #{observer.observer_id}" in summary
    assert "Ресурсов просмотрено: 3" in summary

def test_to_dict_format(observer):
    data = observer.to_dict()
    assert data["observer_id"] == 1
    assert data["fullname"] == "Error Watcher"
    assert data["email"] == "error@lab.com"
    assert isinstance(data["last_accessed"], str)
    assert isinstance(data["access_logs"], dict)
    for value in data["access_logs"].values():
        assert isinstance(value, str)
