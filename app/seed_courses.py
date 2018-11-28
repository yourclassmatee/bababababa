from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def add_course(course_code, sections):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Course')

    response = table.put_item(
        Item={
            'name': course_code,
        }
    )
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

    response = table.update_item(
        Key={
            'name': course_code,
        },
        UpdateExpression="set sections=:s",
        ExpressionAttributeValues={
            ':s': sections
        },
        ReturnValues="UPDATED_NEW"
    )
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

def main():
    # create_user("user 2", "bbb")
    # print(check_password("user 2", "bbb"))

    #add_course("MAT101", [ ["mat101", "F1-5"],["phl101", "W5-6"]])

    sections = [["W_13,W_14", "M_10,M_11", "W_15,W_16"], ["F_13,F_14", "W_13,W_14","Tu_13,Tu_14"],
                ["F_14,F_15", "Tu_14,Tu_15", "W_14,W_15"], ["F_10,F_11", "Th_10,Th_11", "Tu_10,Tu_11"],
                ["F_9,F_10", "Th_14,Th_15", "Tu_12,Tu_13"], ["M_9,M_10", "Th_11,Th_12"],
                ["M_11,M_12", "Th_11,Th_12", "W_11,W_12"], ["M_16,M_17", "Th_16,Th_17", "Tu_17,Tu_18"],
                ["F_13,F_14", "Tu_13,Tu_14", "W_13,W_14"], ["F_16,F_17", "Tu_16,Tu_17", "W_16,W_17"]]
    courses = ["ECE110", "ECE221", "ECE231", "ECE243", "ECE259", "ECE297", "ECE302", "ECE311", "ECE316", "ECE318"]
    for i in range(len(courses)):
        add_course(courses[i], sections[i])

    print("courses added")

if __name__ == "__main__":
    main()