import pytest
import json
from unittest.mock import patch
from application.services.trivia_class import TriviaGame


@pytest.fixture
def mock_api_response():

    return {
        "question": {
            "text": "What is the capital of France?"
        },
        "incorrectAnswers": ["London", "Berlin", "Madrid"],
        "correctAnswer": "Paris"
    }


@patch('requests.get')
def test_load_question(mock_get, mock_api_response):
    """ Tests for load_question, that there is
    one correct answer and three incorrect answers"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = json.dumps([mock_api_response])

    quiz = TriviaGame()

    assert quiz.question["question_text"] == "What is the capital of France?"
    assert quiz.question["correct_answer"] == "Paris"
    assert len(quiz.question["incorrect_answers"]) == 3


@patch('requests.get')
def test_get_question_text(mock_get, mock_api_response):
    """ Tests that the """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = json.dumps([mock_api_response])

    quiz = TriviaGame()


    question_text = quiz.get_question_text()

    assert "What is the capital of France?" in question_text
    assert "Paris" in question_text
    assert "London" in question_text
    assert "Berlin" in question_text
    assert "Madrid" in question_text

    assert any(answer in question_text for answer in ["London", "Berlin", "Madrid", "Paris"])
