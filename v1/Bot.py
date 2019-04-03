from People import People
from Room import Room
from Webhook import Webhook
from Message import Message

import os
import sys


class Bot(People, Room, Webhook, Message):

    def __init__(self):

        # declare headers and how the token will be gotten from the system
        self.URL = "https://api.ciscospark.com/"
        self.auth_token = os.getenv("auth_token")

        if self.auth_token == None:
            sys.exit("'auth_token' not set in the environment variables")
        
        self.headers = {
            "Authorization": "Bearer " + self.auth_token,
            "Content-Type": "application/json"
        }

        # self.hears to function maps when a specific word is heard to a function
        # for example, when one says 'hi' and you want to map it to say_hi() function
        self.hears_to_function = {

        }
        self.attach_function = None

    """
    decorator meant to do a specific action when called
    """
    def on_hears(self, message_text):
        def hear_decorator(f):
            self.hears_to_function[message_text] = f

        return hear_decorator

bot = Bot()

print(
    bot.send_message(
        files=[
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/1200px-Flag_of_Kenya.svg.png"
            ],
        roomId="Y2lzY29zcGFyazovL3VzL1JPT00vNGZjNzliMWItODg3Mi0zYThlLTk3MGItZDNlYmQ4YmI2ZTc3",
        text="Make it"
    )
)

# print(
#     bot.send_message(
#         roomId="Y2lzY29zcGFyazovL3VzL1JPT00vNGZjNzliMWItODg3Mi0zYThlLTk3MGItZDNlYmQ4YmI2ZTc3", text="Not working...",
#     )
# )