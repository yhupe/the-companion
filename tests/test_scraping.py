import pytest
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
from application.services.scraping import get_events, display_events

# Mock HTML content for testing
mock_html = '''
<ul>
    <li class="offer-card">
        <h3>Event 1</h3>
        <div class="offer-date-location">
            <div class="pe-3">
                <div class="bold-italic">2023-10-01</div>
                10:00 AM
            </div>
            <div>Location 1</div>
        </div>
        <div class="richtext-block">Description 1</div>
    </li>
    <li class="offer-card">
        <h3>Event 2</h3>
        <div class="offer-date-location">
            <div class="pe-3">
                <div class="bold-italic">2023-10-02</div>
                11:00 AM
            </div>
            <div>Location 2</div>
        </div>
        <div class="richtext-block">Description 2</div>
    </li>
</ul>
'''


@pytest.fixture
def mock_response():
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.content = mock_html
    return mock_resp


@patch('requests.get')
def test_get_events(mock_get, mock_response):
    mock_get.return_value = mock_response
    events = get_events()
    assert len(events) == 2
    assert events[0]['title'] == 'Event 1'
    assert events[0]['date'] == '2023-10-01'
    assert events[0]['time'] == '10:00 AM'
    assert events[0]['location'] == 'Location 1'
    assert events[0]['description'] == 'Description 1'
    assert events[1]['title'] == 'Event 2'
    assert events[1]['date'] == '2023-10-02'
    assert events[1]['time'] == '11:00 AM'
    assert events[1]['location'] == 'Location 2'
    assert events[1]['description'] == 'Description 2'


def test_display_events(capsys):
    events = [
        {
            "title": "Event 1",
            "date": "2023-10-01",
            "time": "10:00 AM",
            "location": "Location 1",
            "description": "Description 1"
        },
        {
            "title": "Event 2",
            "date": "2023-10-02",
            "time": "11:00 AM",
            "location": "Location 2",
            "description": "Description 2"
        }
    ]
    display_events(events)
    captured = capsys.readouterr()
    assert "Event: Event 1" in captured.out
    assert "When: 2023-10-01" in captured.out
    assert "Time: 10:00 AM" in captured.out
    assert "Where: Location 1" in captured.out
    assert "Description: Description 1" in captured.out
    assert "Event: Event 2" in captured.out
    assert "When: 2023-10-02" in captured.out
    assert "Time: 11:00 AM" in captured.out
    assert "Where: Location 2" in captured.out
    assert "Description: Description 2" in captured.out


def test_display_no_events(capsys):
    display_events([])
    captured = capsys.readouterr()
    assert "Sorry, there are no events for today." in captured.out
