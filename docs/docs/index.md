
# python_webex_bot

A python3 library meant to help you create a cisco webex teams bot and take advantage of some of the features available to these bots. 
Most of the python libraries setup for webex have been lacking in terms of connecting you to a webhook and this aims at solving that

## Installation and setup

The following are items this documentation assumes you already have installed: 
 - virtualenv
 - python3
 - <a href="https://ngrok.com/download">ngrok</a>

### Step 1: setup the virtual environment

to initialize the virtual environment, run the following command in your Command Line or Command Prompt
```
virtualenv venv
```

then we activate it:

<i>Windows</i>
```
venv\Scripts\activate
```

<i>Linux</i>
```
source venv/bin/activate
```

and there, you have your virtual environment setup and ready for action

### Step 2: install python_webex_bot

while still in your activated virtual environment, run the following command to install python_webex_bot via pip:

```
pip install python_webex_bot
```

then download <a href="https://ngrok.com/download">ngrok</a> which will be used in the concurrent steps

## Quickstart

Lets get a simple bot up, running and responsive on our local machine. 

### Step 1: Create the bot on Cisco Webex

If you haven't already, <a href="https://teams.webex.com/signin">create your Webex account.</a> 
Then head on to <a href="https://developer.webex.com/my-apps/new/bot">create your bot</a>

You should be provided with an <u>access token </u> for the bot.

Take this access token and place it in your environment variable as auth_token.

this can be done via your Command prompt or Command Line as:
```
export auth_token=my_auth_token
```

If you're on <i>Windows</i>, run the following on the command prompt:
```
set auth_token=my_auth_token
```

replace my_auth_token with your bots access token

<b>This is a crutial part of running your bot as the python_webex_bot library uses this to identify your bot</b>

If you still have some questions on environment variables, why we need them and how to use them, <a href="https://medium.com/chingu/an-introduction-to-environment-variables-and-how-to-use-them-f602f66d15fa">this</a> may be a good start

### Step 2: setup ngrok

in a different terminal from the one used in steps 1 and 2, navigate to the folder where you have the ngrok placed. 

Then run the following command:
```
ngrok http 5000
```

This should produce an output similar to the one shown below:
```
Session Status                online
Session Expires               7 hours, 59 minutes
Update                        update available (version 2.3.25, Ctrl-U to update)
Version                       2.3.18
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://87a942a1.ngrok.io -> http://localhost:5000
Forwarding                    https://87a942a1.ngrok.io -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

<i>Now you are ready for the quest</i>

### Step 3: create the python file and run it 

Create a python file where you intend to run the bot. In my case, I will name my file `run.py`

copy and paste the following code:

```
from python_webex.v1.Bot import Bot
from python_webex import webhook

bot = Bot()         # the program will automatically know the bot being referred to y the auth_token

# create a webhook to expose it to the internet
# rememer that url we got from step 2, this is where we use it. In my case it was http://87a942a1.ngrok.io. 
# We will be creating a webhook that will be listening when messages are sent
bot.create_webhook(
    name="quickstart_webhook", target_url="http://87a942a1.ngrok.io", resource="messages", event="created"
)

# we create a function that responds when someone says hi
# the room_id will automatically be filled with the webhook. Do not forget it
@bot.on_hears("hi)
def greet_back(room_id=None):
    return bot.send_message(room_id=room_id, text="Hi, how are you doing?")

# We create a default response in case anyone types anything else that we have not set a response for
# this is done using * [ don't ask me what happend when someone sends '*' as the message, that's on my TODO]
@bot.on_hears("*")
def default_response(room_id=None):
    return bot.send_message(room_id=room_id, text="Sorry, could not understand that")


# make the webhook know the bot to be listening for, and we are done
webhook.bot = bot

if __name__ == "__main__":
    webhook.app.run(debug=True)         # don't keep debug=True in production
```

Now, when we text our bot "hi", it will respond with <em>"Hi, how are you doing?"</em>

And when we text anything else, like "When can we meet up?" it will respond with <em>"Sorry, I could not understand that"</em>

# Rooms 

## Get all rooms

<span style="color: orange;">*Always remember that you need to have already set the value <b>auth_token</b> as your bot's Access token before you run this any of the other examples on here.*</span>

What we are aiming to do here is to get all the rooms that the bot is currently in. All from group rooms to individual rooms, we get all the details. Let us look at what we have to do:

```
from python_webex.v1.Bot import Bot

bot = Bot()

all_rooms_response = bot.get_all_rooms()

all_rooms = all_rooms_response.json()

print(all_rooms)

```

If everything works out fine you should see the following output:

```
{
    'items': [
        {
            'title': 'room-title', 
            'ownerId': 'consumer', 
            'id': 'room-id', 
            'teamId': 'team-id', # this will show if it is a group room
            'lastActivity': '2019-03-29T07:36:12.214Z', 
            'created': '2019-03-29T07:34:21.521Z', 
            'isLocked': False, 
            'creatorId': 'creator-id', 
            'type': 'group'
        }
    ]
}
```

## Get room details
<span style="color: orange;">*Always remember that you need to have already set the value <b>auth_token</b> as your bot's Access token before you run this any of the other examples on this tutorial.*</span>

This gets the details of a specific room, we can use the output from <a href="#get-all-rooms">here</a> and get a single rooms ID. We will call the room ID <em>room_id</em>

We will use this <em>room_id</em> to get the details of that specific room, here is how:

```
from python_webex.v1.Bot import Bot

bot = Bot()

room_id = 'someroomid'

room_details_response = bot.get_room_details(room_id=room_id)

room_details = room_details_response.json()

print(room_details)

```

You should see an output similar to this: 

```
{
    'creatorId': 'creator-id', 
    'lastActivity': '2019-03-29T07:36:12.214Z', 
    'id': 'room-id', 
    'title': 'Discussion', 
    'created': '2019-03-29T07:34:21.521Z', 
    'type': 'group', 
    'ownerId': 'consumer', 
    'isLocked': False, 
    'teamId': 'team-id' # if the room is a team
}

```

Use this information wisely. 

## Create Room

<span style="color: orange;">*Always remember that you need to have already set the value <b>auth_token</b> as your bot's Access token before you run this any of the other examples on this tutorial.*</span>

Some of the functionality for creating a room is still being worked on, bear with us. 

The following should work for creating a room:

```
from python_webex.v1.Bot import Bot

bot = Bot()

bot.create_room(title="Bot's room with best friend", team_id="team-id", room_type="something either 'direct' or 'group'")
```

## Update Room Details

<span style="color: orange;">*Always remember that you need to have already set the value <b>auth_token</b> as your bot's Access token before you run this any of the other examples on this tutorial.*</span>

Currently, we can only edit the title of a room. To do so, run the following script:

```
from python_webex.v1.Bot import Bot

bot = Bot()

room_id = 'room-id'

bot.update_room_details(room_id=room_id, title='New Title')
```

## Delete a room

<span style="color: orange;">*Always remember that you need to have already set the value <b>auth_token</b> as your bot's Access token before you run this any of the other examples on this tutorial.*</span>

Let us wreck some havock and delete a room. 

This can be done through:

```
from python_webex.v1.Bot import Bot

bot = Bot()

room_id = 'room-id'

bot.delete_room(room_id=room_id)
```

# Messages

## Get messages

<span style="color: orange;">*Always remember that you need to have already set the value <b>auth_token</b> as your bot's Access token before you run this any of the other examples on this tutorial.*</span>

This lists all the messages that have been received by the bot on a specific room.

This is how we can get these details:

```
from python_webex.v1.Bot import Bot
from pprint import pprint

bot = Bot()

pprint(bot.get_messages(room_id="room-id").json())
```

## Get Direct Messages

<span style="color: orange;">*Always remember that you need to have already set the value <b>auth_token</b> as your bot's Access token before you run this any of the other examples on this tutorial.*</span>

Gets a list of all messages sent in 1:1 rooms. This is basically a list of all the bot's DMs with a particular individual, done by providing the person's ID.

This is how this is done:

```
from python_webex.v1.Bot import Bot
from pprint import pprint

bot = Bot()

pprint(bot.get_direct_messages(person_id="person-id").json())
```

## Get message details

<span style="color: orange;">*Always remember that you need to have already set the value <b>auth_token</b> as your bot's Access token before you run this any of the other examples on this tutorial.*</span>
