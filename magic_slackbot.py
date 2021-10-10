# my slackbot

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
# need to set up the slack events to use Flask web server (where we send the events to)


# loads environment variables from the .env file
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
client.chat_postMessage(channel='#general', text='Hola! Yes, I am alive here too')

if __name__ == "__main__":
    app.run(debug=True)
    # will this thing run in default port, 5000?
    # if I save this file, modify it, I dont need to run the python script again. It will automatically update the web server