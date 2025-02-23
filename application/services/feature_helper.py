from time import sleep
from datetime import datetime

from application.features.journal import JournalHandling
from application.features.trivia_class import TriviaGame
from application.features.open_ai import OpenAI
from application.features.scraping import EventScraper
from application.features.weather_api import get_weather
from application.features.cat import get_cat_image
from application.services.twilio_helper import TwilioMessageService


class FeatureHelper:


    def __init__(self):
        self.tms = TwilioMessageService()

        current_datetime = datetime.now()
        self.current_datetime_str = current_datetime.isoformat()

    def send_trivia_question(self,sender_number) -> None:
        tg = TriviaGame()
        print("initialising Triva")
        question_pack, correct_answer = tg.get_question_text()
        self.tms.send_whatsapp_message(sender_number, question_pack)
        print(question_pack)
        sleep(10)
        self.tms.send_whatsapp_message(sender_number, correct_answer)
        print(correct_answer)

    def get_sentiment_journal(self,sender_number, journal_entry) -> None:
        print("initialising Journal")
        ai = OpenAI()
        mood, advice = ai.get_sentiment_and_advice(journal_entry)
        jh = JournalHandling()
        data = {
            "Date": self.current_datetime_str,
            "Body": journal_entry,
            "mood": mood,
            "advice": advice
        }
        jh.append_storage(data, sender_number)
        self.tms.send_whatsapp_message(sender_number, advice)

    def get_joke(self,sender_number) -> None:
        print("initialising joke")
        ai = OpenAI()
        joke = ai.get_dad_joke()
        print(joke)
        self.tms.send_whatsapp_message(sender_number, joke)

    def get_advice(self,sender_number) -> None:
        print("initialising advice")
        ai = OpenAI()
        advice = ai.get_advice()
        print(advice)
        self.tms.send_whatsapp_message(sender_number, advice)

    def get_activities(self,sender_number) -> None:
        print("initialising activities")
        ws = EventScraper()
        events = ws.display_events()
        print(f"Events retrieved: {events}")
        if events:
            print("Sending WhatsApp message...")
            self.tms.send_whatsapp_message(sender_number, events)
        else:
            print("No events to send.")

    def get_weather_from_api(self,sender_number):
        print("initialising weather")
        weather = get_weather()
        if weather:
            print("Sending WhatsApp message...")
            print(weather)
            self.tms.send_whatsapp_message(sender_number, weather)
            return weather
        else:
            print("No weather info to send.")

    def send_cat_image(self,sender_number: str):
        image_url = get_cat_image()
        if image_url:
            self.tms.send_whatsapp_message(sender_number, image_url)
        else:
            print("Failed to get a cat image.")
