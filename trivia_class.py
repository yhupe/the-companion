import requests
import json
import random

class TriviaGame:
    """Handles the trivia game and manages questions"""

    API_URL = "https://the-trivia-api.com/v2/questions/"

    def __init__(self):
        self.question = None
        self.load_question()
        self.correct_index = None

    def load_question(self):
        """Loads a question"""
        response = requests.get(self.API_URL)

        if response.status_code != requests.codes.ok:
            print("Error:", response.status_code, response.text)
            exit()

        question_data = json.loads(response.text)

        item = question_data[0]

        self.question = {
            "question_text": item["question"]["text"],
            "incorrect_answers": item["incorrectAnswers"],
            "correct_answer": item["correctAnswer"]
        }

    def get_question_text(self):
        """Returns question all 4 possible answers and at least the right solution separately """

        question_text = self.question["question_text"]
        incorrect_answers = self.question["incorrect_answers"]
        correct_answer = self.question["correct_answer"]

        answers = incorrect_answers + [correct_answer]
        random.shuffle(answers)
        self.correct_index = answers.index(correct_answer) + 1

        question_pack = f"""
{question_text}
{"\n".join(f"{i+1}. {item}" for i, item in enumerate(answers))}
"""

        return question_pack

    def is_correct(self, user_choice):

        return int(user_choice) == self.correct_index

if __name__ == "__main__":
    quiz = TriviaGame()
    question_text = quiz.get_question_text()
    print(question_text)
    print(quiz.is_correct("3"))