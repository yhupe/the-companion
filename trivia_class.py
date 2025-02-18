import requests
import json
import random


class Question:
    """Represents one single question"""

    def __init__(self, question_text, incorrect_answers, correct_answer):
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.answers = incorrect_answers + [correct_answer]
        random.shuffle(self.answers)

    def display(self):
        """Prints the question and all possible choices"""
        print(self.question_text)
        for index, answer in enumerate(self.answers, start=1):
            print(f"{index}: {answer}")

    def is_correct(self, user_choice):
        """Checks whether user choice is right or wrong"""
        try:
            user_choice_index = int(user_choice) - 1
            return self.answers[user_choice_index] == self.correct_answer
        except (ValueError, IndexError):
            return False


class TriviaGame:
    """Handles the trivia game"""

    API_URL = "https://the-trivia-api.com/v2/questions/"

    def __init__(self, rounds):
        self.questions = []
        self.rounds = rounds
        self.load_questions()

    def load_questions(self):
        """Loads questions and saves them"""
        response = requests.get(self.API_URL)

        if response.status_code != requests.codes.ok:
            print("Error:", response.status_code, response.text)
            exit()

        question_data = json.loads(response.text)

        self.questions = [
            Question(
                item["question"]["text"],
                item["incorrectAnswers"],
                item["correctAnswer"],
            )
            for item in question_data
        ]

    def play(self):
        """Starts the game"""
        print("\n🎉 Welcome to a round of trivia! 🎉\n")

        score = 0
        rounds_played = 0

        while rounds_played < self.rounds:
            question = self.questions[rounds_played % len(self.questions)]
            question.display()

            user_answer = input("\nWhich answer do you think is correct? (Enter a number 1-4 or 'exit' to quit): ").strip()

            if user_answer.lower() == 'exit':
                print("❌ The game has ended.")
                break

            if question.is_correct(user_answer):
                print("✅ Correct! 🎉\n")
                score += 1
            else:
                print(f"❌ Unfortunately you are wrong! The correct answer is: {question.correct_answer}\n")

            rounds_played += 1

        print(f"🏆 You answered {score} out of {self.rounds} questions correctly!")


def get_rounds():
    """Asks the user how many rounds they want to play (1 to 10)."""
    while True:
        try:
            rounds = int(input("How many rounds would you like to play? (1 to 10): "))
            if 1 <= rounds <= 10:
                return rounds
            else:
                print("❌ Please enter a number between 1 and 10.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


if __name__ == "__main__":
    rounds = get_rounds()
    quiz = TriviaGame(rounds)
    quiz.play()