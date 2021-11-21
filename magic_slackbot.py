# my slackbot

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request 
from slackeventsapi import SlackEventAdapter
from flask import jsonify
import boto3
from boto3.dynamodb.conditions import Key

# loads environment variables from the .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)


#test_electives = {'IDS601': 'Took with Akande, goes fast throughout the whole semester. Be familiar with distributions and how to manipulate them'}



slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

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

@app.route('/dynamo/<msg2>')
def send3(msg2):
    text = 'IDS 602'
    print(f"Send message dynamodb {msg2}")
    class_feedback = query_table(text)
    print_statements = digest(class_feedback)
    return jsonify(print_statements)
  
# ______________________________________________________________________________________________________ 
# QUERYING TABLES
 
def query_table(class_number):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    print(class_number)
    table = dynamodb.Table('CLASSES')
    response = table.query(
        KeyConditionExpression=Key('class_name').eq(class_number)
    )
    print(response['Items'])
    return response['Items']
    
def digest(class_feedback):
    number_statement = f'There are {len(class_feedback)} students in MIDS who have taken this elective.'
    participants = []
    feedback = []
    for i in class_feedback:
        participants.append(i['student_name'])
        feedback.append(i['feedback'])
        pass
    participants_joined = ', '.join(participants)
    participants_statement = f"The MIDS students who have taken this elective are: {participants_joined}."
    feedback_statement = ''
    for i in range(len(class_feedback)):
        feedback_statement += (participants[i] + ' gave the feedback: ' + feedback[i] + '\n')
        pass
    feedback_statement = feedback_statement [:-1]
    return number_statement, participants_statement, feedback_statement
    
 
# HANDLING MESSAGES
# This is the route that will collect variables and handle message payload:

@slack_event_adapter.on('message')
def message(payload):
    """ This is trying to capture whatever is in the EVENT in the message.channel payload, otherwise assigns an empty dictionary {} """
    event = payload.get('event', {}) 
    channel_id = event.get('channel')
    user_id = event.get('user')
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text='Please contact Noah Gift for help')

#HANDLING EVENTS
# Status 200 means "all good"
@app.route('/elective', methods=['POST'])
def elective():
    data = request.form
    user_id = data.get('used_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    print(text)
    #class_feedback = test_electives.get(text,0)
    class_feedback = query_table(text)
    print_statements = digest(class_feedback)
    print(print_statements)
    for i in print_statements:
        client.chat_postMessage(channel=channel_id, text=i)
    return Response(), 200
    
@app.route('/addfeedback', methods=['POST'])
def addfeedback():
    data = request.form
    user_id = data.get('used_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    print(text) #"Clarissa Ache, IDS 405, I hated this class, 1"
    feedback_list = text.split('; ')
    feedback_dict = {'student_name': feedback_list[0], 'class_name': feedback_list[1], 'feedback': feedback_list[2], 'rating': feedback_list[3]}
    send_to_dynamo(feedback_dict)
    client.chat_postMessage(channel=channel_id, text="Your feedback has been recorded. You are loved and your feelings are valid.")
    return Response(), 200

def send_to_dynamo(feedback_dict):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('CLASSES')
    response = table.put_item(
       Item = feedback_dict
    )
    pass



if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
    # will this thing run in default port, 5000?
    # "debug" : if I save this file, modify it, I dont need to run the python script again. It will automatically update the web server