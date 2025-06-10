import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
import numpy as np


@pytest.fixture
def client():
    return TestClient(app)


@patch("app.main.rss.fetch_feed")
@patch("app.main.neo4j")
@patch("app.main.nlp")
@patch("app.main.clustering.find_or_create_theme")
def test_ingest_feed(
    mock_find_or_create_theme,
    mock_nlp,
    mock_neo4j,
    mock_fetch_feed,
    client
):
    # Setup mock feed entry
    entry = MagicMock()
    entry.link = "http://example.com/post"
    entry.title = "Example Post"
    entry.summary = "This is a test. It has thesis."
    entry.published_parsed = (2024, 1, 1, 0, 0, 0, 0, 0, 0)
    mock_fetch_feed.return_value = [entry]

    mock_neo4j.fetch_all_post_urls.return_value = []
    mock_nlp.extract_thesis.return_value = ["This is a thesis"]
    mock_nlp.model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
    mock_neo4j.fetch_all_theses.return_value = []
    mock_find_or_create_theme.return_value = "theme-1"

    response = client.post("/ingest", json="http://example.com/feed")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["new_posts"] == 1

    mock_fetch_feed.assert_called_once()
    mock_neo4j.ingest_post.assert_called_once()
    mock_nlp.extract_thesis.assert_called_once()


@patch("app.main.neo4j")
def test_get_themes(mock_neo4j, client):
    mock_neo4j.get_all_themes.return_value = [{"theme_id": "t1", "text": "Example"}]

    response = client.get("/themes")

    assert response.status_code == 200
    assert response.json() == [{"theme_id": "t1", "text": "Example"}]


@patch("app.main.neo4j")
def test_get_theme_timeline(mock_neo4j, client):
    mock_neo4j.get_theme_timeline.return_value = [
        {"url": "http://example.com", "timestamp": "2024-01-01T00:00:00"}
    ]

    response = client.get("/themes/theme-1")

    assert response.status_code == 200
    assert response.json() == [{"url": "http://example.com", "timestamp": "2024-01-01T00:00:00"}]
