import boto3
from boto3.dynamodb.conditions import Key


def query_table(class_number, dynamodb=None):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('MIDS')
    response = table.query(
        KeyConditionExpression=Key('class_number').eq(class_number)
    )
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


if __name__ == '__main__':
    class_number = 'IDS xxx'
    json_list = query_table(class_number)
    print_statements = digest(json_list)
    print(print_statements[0])