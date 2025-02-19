import os
import time

from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from datetime import datetime
from application.services.message_handling import MessageHandling
from application.services.journal import JournalHandling
from application.services.trivia_class import TriviaGame
from application.services.open_ai import OpenAI
from application.services.scraping import EventScraper
from application.services.cat import get_cat_image
from application.services.Weather_api import get_weather

WhatsAppNumber = str

whatsapp = Blueprint("whatsapp", __name__)




TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

current_datetime = datetime.now()
current_datetime_str = current_datetime.isoformat()

COMMANDS = {
    "help": """Available commands: 
    help, 
    weather, 
    journal <journal entry>, 
    activities, 
    advice, 
    trivia,
    joke""",
    "trivia": "Let me ask you a trivia question  😆",
    "activities": "Let me see what's going on in your area",
    "advice": "Advice is luckily something you can ignore 😅",
    "journal": "Tell me about your day - what was good, what was not so good",
    "weather": "Let me check what the weather is like in your area",
    "joke": "Let me tell you a dad joke 😂",
    "cat" : "Old people are cat people"
}


def process_command(message):
    words = message.strip().lower().split()
    if not words:
        return "I didn't catch that. Try sending 'help' for options."
    command = words[0]
    return words[0], COMMANDS.get(command, "Unknown command. Send 'help' for options.")



@whatsapp.route("/whatsapp_incoming", methods=["POST"])
def whatsapp_incoming():
    dh = MessageHandling()

    incoming_message = request.form.get("Body")
    sender_number = request.form.get("From")

    print(f"Incoming Message from {sender_number} : {incoming_message}")
    data = {
        "Date":current_datetime_str,
        "Body": incoming_message
    }
    dh.append_storage(data,sender_number,)
    command, response_text = process_command(incoming_message)
    print(command, response_text)

    twilio_response = MessagingResponse()

    match command:
        case "trivia":

            send_whatsapp_message(sender_number,response_text)
            send_trivia_question(sender_number)
        case "journal":
            get_sentiment_journal(sender_number,incoming_message)
        case "joke":
            send_whatsapp_message(sender_number, response_text)
            get_joke(sender_number)
        case "activities":
            send_whatsapp_message(sender_number, response_text)
            get_activities(sender_number)
        case "advice":
            send_whatsapp_message(sender_number, response_text)
            get_advice(sender_number)
        case "cat":
            send_whatsapp_message(sender_number, response_text)
            send_cat_image(sender_number)
        case "weather":
            send_whatsapp_message(sender_number, response_text)
            get_weather_from_api(sender_number)



        case _ :
            twilio_response.message(response_text)

    return str(twilio_response)


@whatsapp.route("/whatsapp_status_callback", methods=["POST"])
def whatsapp_status_callback():
    status = request.form.get("MessageStatus")
    message_sid = request.form.get("MessageSid")

    print(f"Message SID: {message_sid}, Status: {status}")

    return "", 200

def send_trivia_question(sender_number)-> None:
    tg = TriviaGame()
    print("initialising Triva")
    question_pack,correct_answer = tg.get_question_text()
    send_whatsapp_message(sender_number, question_pack)
    print(question_pack)
    time.sleep(10)
    send_whatsapp_message(sender_number, correct_answer)
    print(correct_answer)

def get_sentiment_journal(sender_number, journal_entry)->None:
    print("initialising Journal")
    ai = OpenAI()
    mood, advice = ai.get_sentiment_and_advice(journal_entry)
    jh = JournalHandling()
    data = {
        "Date": current_datetime_str,
        "Body": journal_entry,
        "mood": mood,
        "advice":advice
    }
    jh.append_storage(data, sender_number)
    send_whatsapp_message(sender_number, advice)

def get_joke(sender_number) -> None:
    print("initialising joke")
    ai = OpenAI()
    joke = ai.get_dad_joke()
    send_whatsapp_message(sender_number, joke)

def get_advice(sender_number) -> None:
    print("initialising advice")
    ai = OpenAI()
    advice = ai.get_advice()
    send_whatsapp_message(sender_number, advice)

def get_activities(sender_number) -> None:
    print("initialising activities")
    ws = EventScraper()
    events = ws.display_events()
    print(f"Events retrieved: {events}")
    if events:
        print("Sending WhatsApp message...")
        send_whatsapp_message(sender_number, events)
    else:
        print("No events to send.")

def get_weather_from_api(sender_number):
    print("initialising weather")
    weather = get_weather()
    if weather:
        print("Sending WhatsApp message...")
        send_whatsapp_message(sender_number, weather)
        return weather
    else:
        print("No weather info to send.")




def send_cat_image(sender_number: str):
    image_url = get_cat_image()  # Get cat image URL
    if image_url:
        send_whatsapp_image(sender_number, image_url)  # Send it via Twilio
    else:
        print("Failed to get a cat image.")

def send_whatsapp_image(sender_number: str, image_url: str):
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=sender_number,
        media_url=[image_url]  # The image URL from the API response
    )
    print(f"Image sent with SID: {message.sid}")
    return message.sid


def send_whatsapp_message(sender_number:WhatsAppNumber ,  message_body:str):
    print(f"Sending message to: {sender_number}")
    print(f"Message content: {message_body}")

    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=sender_number,
        body=message_body
    )
    print(f"Message sent with SID: {message.sid}")
    return message.sid


