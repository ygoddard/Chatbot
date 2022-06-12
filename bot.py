import os
from enum import Enum

import requests
from flask import Flask, request, jsonify, session
from config import Config
from database.mongo import MongoDbProvider
from datetime import datetime
from messages.twilio import TwilioMessagesProvider


class Responses:
    OK = '', 200


class WebApp():
    def __init__(self, ip='localhost', port=8000, debug=True):
        self.app = Flask(__name__)
        self.config = Config("config/main_config.yaml")
        self.db = MongoDbProvider(self.app, self.config)
        self.messages = TwilioMessagesProvider(self.app, self.config)
        self.ip = ip
        self.port = port
        self.debug = debug

    def run(self):
        @self.app.route('/bot', methods=['POST'])
        def bot():
            incoming_msg = request.values.get('Body', '').lower()

            whatsapp_id = request.values.get('WaId', None)
            if whatsapp_id == None:
                print(f'No whatsapp id: {request.values}')
                return

            profile_name = request.values.get('ProfileName', 'Anonimus')
            contact = self.db.find_one({"whatsapp_id": whatsapp_id})
            new_session = False
            curr_datetime = datetime.now()
            if contact == None:
                doc = {
                    "whatsapp_id": whatsapp_id,
                    "last_session": curr_datetime
                }
                self.db.insert(doc)
                new_session = True
            else:
                if (curr_datetime - contact['last_session']).total_seconds() > self.config.session_dead_threshold_in_sec:
                    # Update last session
                    self.db.update_one({"_id": contact['_id']}, {"$set": {"last_session": curr_datetime}})
                    new_session = True

            if new_session:
                self.messages.send_text(_from=request.values['To'],
                                        _to=request.values['From'],
                                        text=f'Hello {profile_name},\nIts your first time here.\nChoose one of the following actions:\n1. Information\n2. Scheduale abseiling date',
                                        )

                return Responses.OK

            if incoming_msg == '1':
                self.messages.send_text(_from=request.values['To'],
                                           _to=request.values['From'],
                                           text=f'Information is blah blah'
                                           )
            elif incoming_msg == '2':
                self.messages.send_text(_from=request.values['To'],
                                           _to=request.values['From'],
                                           text=f'Enter a date.....'
                                           )
            return Responses.OK

        self.app.run(self.ip, self.port, self.debug)


if __name__ == '__main__':
    webapp = WebApp(ip='localhost', port=5000, debug=True)
    webapp.run()