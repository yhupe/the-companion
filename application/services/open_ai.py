from openai import OpenAI
import os
from flask.cli import load_dotenv

load_dotenv()


class OpenAI:

    def __init__(self,):

        # self.client = OpenAI(
        #     api_key=os.environ.get("OPENAI_API_KEY"),
        # )

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
        completion = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system",
                 "content": content},
                {"role": "user", "content": text}
                ]
            )
        response = completion.choices[0].message.content
        mood, advice = response.split('.', 1)
        mood = mood.strip()
        advice = advice.strip()
        print(mood)
        print(advice)

        return mood,advice


# ai = OpenAI()
# text = "I feel really stressed out and anxious. My work is overwhelming, and I don’t have enough time for myself."
# sentiment_advice = ai.get_sentiment_and_advice(text)
# print(sentiment_advice)
