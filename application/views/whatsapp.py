from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
from application.app import app
from application.services.data_base_handling import DataHandling

whatsapp = Blueprint("whatsapp", __name__)

dh = DataHandling()

COMMANDS = {
    "help": "Available commands: help, weather, journal, activities, advice, trivia",
    "trivia": "Let me ask you a trivia question  😆",
    "activities": "Let me see what's going on in your area",
    "advice": "Always code as if the person maintaining it is a violent psychopath who knows where you live. 😅",
    "journal": "Tell me about your day - what was good, what was not so good",
    "weather": "Let me check what the weather is like in your area"
}


def process_command(message):
    words = message.strip().lower().split()
    if not words:
        return "I didn't catch that. Try sending 'help' for options."
    command = words[0]
    return COMMANDS.get(command, "Unknown command. Send 'help' for options.")



@whatsapp.route("/whatsapp_incoming", methods=["POST"])
def whatsapp_incoming():

    incoming_message = request.form.get("Body")
    sender_number = request.form.get("From")
    current_datetime = datetime.now()
    app.logger.info(f"Incoming WhatsApp from {sender_number}")
    data = {
        "Date":current_datetime,
        "Body": incoming_message
    }
    dh.append_storage(sender_number, data)
    response_text = process_command(incoming_message)

    twilio_response = MessagingResponse()
    twilio_response.message(response_text)

    return str(twilio_response)


@whatsapp.route("/whatsapp_status_callback", methods=["POST"])
def whatsapp_status_callback():
    status = request.form.get("MessageStatus")
    message_sid = request.form.get("MessageSid")

    print(f"Message SID: {message_sid}, Status: {status}")

    return "", 200
