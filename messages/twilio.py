from .provider import MessagesProvider
from twilio.rest import Client
import os
from twilio.twiml.messaging_response import MessagingResponse


class TwilioMessagesProvider(MessagesProvider):
    def __init__(self, app, config):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(account_sid, auth_token)

    def send_text(self, text: str, _from: str, _to: str):
        return self.client.messages.create(
                        from_=_from,
                        to=_to,
                        body=text
                    )

    def send_multimedia(self, text: str, media_url: str, _from: str, _to: str):
        return self.client.messages.create(
                        from_=_from,
                        to=_to,
                        body=text,
                        media_url=media_url
                    )