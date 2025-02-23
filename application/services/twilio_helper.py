from twilio.rest import Client
import os

WhatsAppNumber = str
MessageSID = str


class TwilioMessageService:


    def __init__(self):

        self.TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
        TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)



    def send_whatsapp_image(self,sender_number: str, image_url: str) -> MessageSID:
        """function for sending images"""
        message = self.client.messages.create(
            from_=self.TWILIO_WHATSAPP_NUMBER,
            to=sender_number,
            media_url=[image_url]
        )
        print(f"Image sent with SID: {message.sid}")
        return message.sid

    def send_whatsapp_message(self,sender_number: WhatsAppNumber, message_body: str) -> MessageSID:
        """function for sending messages"""
        message = self.client.messages.create(
            from_=self.TWILIO_WHATSAPP_NUMBER,
            to=sender_number,
            body=message_body
        )
        print(f"Message sent with SID: {message.sid}")
        return message.sid
