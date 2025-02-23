

from flask import Blueprint, request

from application.services.function_helper import CompanionFeatures
from twilio.twiml.messaging_response import MessagingResponse

whatsapp = Blueprint("whatsapp", __name__)



@whatsapp.route("/whatsapp_incoming", methods=["POST"])
def whatsapp_incoming():
    cf = CompanionFeatures()

    incoming_message = request.form.get("Body")
    sender_number = request.form.get("From")
    cf.log_messages(sender_number=sender_number, incoming_message=incoming_message)
    cf.process_command(sender_number=sender_number, incoming_message=incoming_message)

    return str(f"Message received from {sender_number}"), 200


@whatsapp.route("/whatsapp_status_callback", methods=["POST"])
def whatsapp_status_callback():
    status = request.form.get("MessageStatus")
    message_sid = request.form.get("MessageSid")

    print(f"Message SID: {message_sid}, Status: {status}")

    return "", 200






