# my slackbot

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request 
from slackeventsapi import SlackEventAdapter
from flask import jsonify

# loads environment variables from the .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)


test_electives = {'IDS601': 'Took with Akande, goes fast throughout the whole semester. Be familiar with distributions and how to manipulate them'}



slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']


# ______________________________________ For testing purposes _________________________________________
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Hello World!'


@app.route('/slack2/<msg>')
def send2(msg):
    print(f"Send message {msg}")
    client.chat_postMessage(channel='#general', text=f'{msg}')
    return jsonify(msg)
 
# ______________________________________________________________________________________________________ 
 
 
# HANDLING MESSAGES
# This is the route that will collect variables and handle message payload:

@slack_event_adapter.on('message')
def message(payload):
    """ This is trying to capture whatever is in the EVENT in the message.channel payload, otherwise assigns an empty dictionary {} """
    event = payload.get('event', {}) 
    channel_id = event.get('channel')
    user_id = event.get('user')
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text='Hola! I do not understand your message yet. Please donate $1000 to @clarissaache so I can learn how chat')

#HANDLING EVENTS
# Status 200 means "all good"
@app.route('/elective', methods=['POST'])
def elective():
    data = request.form
    user_id = data.get('used_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    client.chat_postMessage(channel=channel_id, text='I got your command. We are working on giving you a summary of all the feedback from students who have taken this class')
    return Response(), 200



if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
    # will this thing run in default port, 5000?
    # "debug" : if I save this file, modify it, I dont need to run the python script again. It will automatically update the web server