import requests
import json

api_url = "https://the-trivia-api.com/v2/questions/?"


response = requests.get(api_url)
list_of_dicts = json.loads(response.text)

if response.status_code == requests.codes.ok:
    pass
else:
    print("Error:", response.status_code, response.text)


def get_one_question(response_from_url):

    for question_pack in response_from_url:
        print(question_pack['question'] ['text'])
        correct_answer = question_pack['correctAnswer']
        list_of_incorrect_answers = question_pack['incorrectAnswers']

        for answer in list_of_incorrect_answers:
            print(f"incorrect answers: {answer}")

        print(f"correct answer: {correct_answer}")

        print(70 * "*")




def main():
    get_one_question(list_of_dicts)



if __name__ == '__main__':
    main()