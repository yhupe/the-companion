from datetime import datetime

from application.services.twilio_helper import TwilioMessageService
from application.services.message_handling import MessageHandling
from application.services.feature_helper import FeatureHelper

class CompanionFeatures:

    def __init__ (self):

        self.tms = TwilioMessageService()
        self.dh = MessageHandling()
        self.feature = FeatureHelper()
        current_datetime = datetime.now()
        self.current_datetime_str = current_datetime.isoformat()



        self.COMMANDS = {
            "help": ["""Available commands: 
            help, 
            weather, 
            journal <journal entry>, 
            activities, 
            advice, 
            trivia,
            joke""",
                     None],
            "trivia": [
                "Let me ask you a trivia question  😆",
                self.feature.send_trivia_question],
            "activities":[
                "Let me see what's going on in your area",
                self.feature.get_activities],
            "advice": ["Advice is luckily something you can ignore 😅",
                       self.feature.get_advice],
            "journal": [
                "Tell me about your day - what was good, what was not so good",
                self.feature.get_sentiment_journal],
            "weather": ["Let me check what the weather is like in your area",
                        self.feature.get_weather_from_api],
            "joke": [
                "Let me tell you a dad joke 😂",
                self.feature.get_joke],
            "cat": [
                "Old people are cat people",
            self.feature.send_cat_image]
        }

    def process_command(self,sender_number, incoming_message):
        words = incoming_message.strip().lower().split()
        if not words:
            return "I didn't catch that. Try sending 'help' for options."
        command = words[0]
        if command not in self.COMMANDS.keys():
            send_message = "Unknown command. Send 'help' for options."
            print(f"sending message {send_message}")
            self.tms.send_whatsapp_message(sender_number=sender_number,
                                           message_body=send_message)
        else:
            send_message = self.COMMANDS[command][0]
            func = self.COMMANDS[command][1]
            print(f"{command} received - trying to execute {func}")
            print(f"sending message {send_message}")
            self.tms.send_whatsapp_message(sender_number=sender_number,message_body = send_message )
            if not func:
                send_message = "Unknown command. Send 'help' for options."
                print(f"sending message {send_message}")
                self.tms.send_whatsapp_message(sender_number=sender_number,message_body = send_message )
            elif command == "journal":
                func(sender_number, incoming_message)
            else:
                func(sender_number)


    def log_messages(self, sender_number, incoming_message):
        print(f"Incoming Message from {sender_number} : {incoming_message}")
        data = {
            "Date": self.current_datetime_str,
            "Body": incoming_message
        }
        self.dh.append_storage(data, sender_number, )
