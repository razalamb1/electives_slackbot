import pandas as pd
import boto3
from boto3.dynamodb.conditions import Key


feedbacks = pd.read_excel("CourseList.xlsx")
feedbacks.fillna("", inplace = True)
feedbacks["rating"] = feedbacks["rating"].astype(str)
print(feedbacks.dtypes)
dicts = feedbacks.to_dict(orient = "index")
length = feedbacks.shape[0]
for i in range (0, length):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    feedback = dicts[i]
    if feedback["student_name"] == "":
        continue
    print(feedback)
    table = dynamodb.Table('CLASSES')
    response = table.put_item(
       Item = feedback
    )
    pass
