from flask import Blueprint, request

whatsapp = Blueprint("whatsapp", __name__)

@whatsapp.route("/whatsapp_incoming", methods=["POST"])
def whatsapp_incoming():
    incoming_message = request.form.get("Body")
    sender_number = request.form.get("From")
    print(f"Received message: {incoming_message} from {sender_number}")
    return '<Response><Message>Thank you for your message!</Message></Response>'


@whatsapp.route("/whatsapp_status_callback", methods=["POST"])
def whatsapp_status_callback():
    status = request.form.get("MessageStatus")
    message_sid = request.form.get("MessageSid")

    print(f"Message SID: {message_sid}, Status: {status}")

    return "", 200
