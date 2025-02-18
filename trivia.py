import requests
import json
import random

api_url = "https://the-trivia-api.com/v2/questions/"

response = requests.get(api_url)
list_of_dicts = json.loads(response.text)

if response.status_code != requests.codes.ok:
    print("Error:", response.status_code, response.text)
    exit()


def get_one_question(response_from_url):
    random_question = random.randint(0, len(response_from_url) - 1)
    one_question_pack = response_from_url[random_question]

    question = one_question_pack['question']['text']
    incorrect_answers = one_question_pack['incorrectAnswers']
    correct_answer = one_question_pack['correctAnswer']

    return question, incorrect_answers, correct_answer


def ask_question(question, incorrect_answers, correct_answer):
    choice_list = incorrect_answers + [correct_answer]
    random.shuffle(choice_list)

    choice_list_with_index = [f"{i + 1}: {answer}" for i, answer in enumerate(choice_list)]

    return question, choice_list_with_index, correct_answer


def main():
    question, choice_list_with_index, correct_answer = ask_question(*get_one_question(list_of_dicts))

    print(question)
    for answer in choice_list_with_index:
        print(answer)

    user_answer = input("Which of these do you think is correct? (enter 1, 2, 3 or 4): ").strip()

    try:
        user_choice_index = int(user_answer) - 1
        chosen_answer = choice_list_with_index[user_choice_index][3:]

        if chosen_answer == correct_answer:
            print("✅ Correct! Yuhuu! 🎉")
        else:
            print(f"❌ Wrong! The correct answer is: {correct_answer}")
    except (ValueError, IndexError):
        print("❌ Invalid answer... please enter a number 1-4")


if __name__ == "__main__":
    main()