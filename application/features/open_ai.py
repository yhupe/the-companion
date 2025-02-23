
import os
from flask.cli import load_dotenv
import openai

load_dotenv()


class OpenAI:

    def __init__(self):

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.MODEL="gpt-4o-mini"


    def get_sentiment_and_advice(self,text):
        content = """
        You are a helpful assistant focused on the well-being of others. 
        Categorize the mood of the text as either "positive", "negative", or "neutral". 
        Return the result in the following format:
        A single word category (either "positive", "negative", or "neutral").
        Followed by advice on how to improve the mood, written clearly and concisely.
        Ensure the response always includes both the category and the advice.
        """
        completion = openai.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system",
                 "content": content},
                {"role": "user", "content": text}
                ]
            )
        response = completion.choices[0].message.content
        print(response)
        mood, advice = response.split('\n', 1)
        mood = mood.strip()
        advice = advice.strip()
        print(mood)
        print(advice)

        return mood,advice

    def get_dad_joke(self):
        content = """
        You are a witty dad who loves telling those groaning dad jokes.
        Make someone laught with a genius dad joke or pun
        """
        completion = openai.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system",
                 "content": content},
                {"role": "user", "content": "Tell me a dad joke or pun"}
                ]
            )
        response = completion.choices[0].message.content
        print(response)
        return response

    def get_advice(self):
        content = """
        You are a witty dad who loves giving useless and funny advice.
        """
        completion = openai.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system",
                 "content": content},
                {"role": "user", "content": "Give me some one piece of advice to laugh about"}
                ]
            )
        response = completion.choices[0].message.content
        print(response)
        return response


