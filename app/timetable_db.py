from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr
from werkzeug.security import generate_password_hash, check_password_hash
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def create_user_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='User',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            # {
            #     'AttributeName': 'password',
            #     'AttributeType': 'S'
            # },
            # {
            #     'AttributeName': 'timetable',
            #     'AttributeType': 'L'
            # },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("user Table status:", table.table_status)

def create_course_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.create_table(
        TableName='Course',
        KeySchema=[
            {
                'AttributeName': 'course_code',
                'KeyType': 'HASH'  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'course_code',
                'AttributeType': 'S'
            },
            # {
            #     'AttributeName': 'sections',
            #     'AttributeType': 'L' #list
            # },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("course Table status:", table.table_status)

def check_password(name, password):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('User')
    response = table.query(
        KeyConditionExpression=Key('name').eq(name)
    )
    items = response['Items']
    if items:
        # user exist
        response = table.get_item(
                Key={
                    'name': name,
                }
            )
        if response['Item']['password'] == generate_password_hash(password):
            return 0
        else:
            #wrong password
            return 1
    else:
        #user not exist
        return 2

def find_user(name):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('User')
    response = table.query(
        KeyConditionExpression=Key('name').eq(name)
    )
    items = response['Items']
    if items:
        return True
    else:
        # user not exist
        return False

def create_user(name, password):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('User')
    response = table.put_item(
       Item={
            'name': name
            }
    )

    # add password attribute
    response = table.update_item(
        Key={
            'name': name,
        },
        UpdateExpression="set  password=:p",
        ExpressionAttributeValues={
            ':p': generate_password_hash(password)
        },
        ReturnValues="UPDATED_NEW"
    )

    print("UpdateItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))


def add_course(course_code, sections):
    # sections format: [["mat101", "F1-5"], ["phl101","W5-6"]]
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Course')

    # course_code = "MAT101"
    # section = ["F1-3", "M3-4"]

    response = table.put_item(
        Item={
            'course_code': course_code,
        }
    )
    #print(json.dumps(response, indent=4, cls=DecimalEncoder))

    response = table.update_item(
        Key={
            'course_code': course_code,
        },
        UpdateExpression="set  sections=:s",
        ExpressionAttributeValues={
            ':s': {
                "L": sections
                # "L": [
                #     ["mat101", "F1-5"],
                #     ["phl101", "W5-6"]
                # ]
            },



        },
        ReturnValues="UPDATED_NEW"
    )
    #print(json.dumps(response, indent=4, cls=DecimalEncoder))

