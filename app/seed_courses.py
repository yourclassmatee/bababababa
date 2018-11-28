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


def add_no_conflict():
    #410,552,421,343,568->196, 431
    sections = [["M_9,M_11", "Tu_9,Tu_11"], ["W_12,W_14", "Th_13,Th_15"],
                ["Tu_9,Tu_11", "M_14,M_16"], ["Th_11,Th_12", "Th_12,Th_13"],
                ["Tu_12,Tu_14", "Tu_15,Tu_17"], ["M_14,M_16", "Tu_10,Tu_12"],
                ["Th_14,Th_16", "F_13,F_15"]]
    courses = ["ECE410", "ECE421", "ECE431", "ECE343", "ECE196", "ECE552", "ECE568"]
    for i in range(len(courses)):
        add_course(courses[i], sections[i])

    print("add no conflict")

def add_no_friday():
    sections = [["Tu_12,Tu_14", "Tu_15,Tu_17"], ["Tu_9,Tu_11", "M_14,M_16"]]
    courses = ["ECE196", "ECE431"]
    for i in range(len(courses)):
        add_course(courses[i], sections[i])

    print("add no friday")

def add_conflict():
    #410,444,418,421,343->196, 431
    # sections = [["M_9,M_11", "Tu_9,Tu_11"], ["W_12,W_14", "Th_13,Th_15"],
    #             ["F_9,F_11", "M_14,M_16"], ["Th_11,Th_12", "Th_12,Th_13"],
    #             ["F_12,F_14", "Tu_13,Tu_15"], ["Tu_12,Tu_14"],
    #             ["Tu_13,Tu_15"]]
    # courses = ["ECE410", "ECE421", "ECE431", "ECE343", "ECE196", "ECE418", "ECE444"]
    sections = [["Tu_12,Tu_14"],["Tu_13,Tu_15"]]
    courses = ["ECE418", "ECE444"]
    for i in range(len(courses)):
        add_course(courses[i], sections[i])

    print("add conflict")

def main():
    # sections = [["W_13,W_14", "M_10,M_11", "W_15,W_16"], ["F_13,F_14", "W_13,W_14","Tu_13,Tu_14"],
    #             ["F_14,F_15", "Tu_14,Tu_15", "W_14,W_15"], ["F_10,F_11", "Th_10,Th_11", "Tu_10,Tu_11"],
    #             ["F_9,F_10", "Th_14,Th_15", "Tu_12,Tu_13"], ["M_9,M_10", "Th_11,Th_12"],
    #             ["M_11,M_12", "Th_11,Th_12", "W_11,W_12"], ["M_16,M_17", "Th_16,Th_17", "Tu_17,Tu_18"],
    #             ["F_13,F_14", "Tu_13,Tu_14", "W_13,W_14"], ["F_16,F_17", "Tu_16,Tu_17", "W_16,W_17"]]
    # courses = ["ECE110", "ECE221", "ECE231", "ECE243", "ECE259", "ECE297", "ECE302", "ECE311", "ECE316", "ECE318"]
    # for i in range(len(courses)):
    #     add_course(courses[i], sections[i])
    #
    # print("courses added")
    #add_no_conflict()
    #add_conflict()
    add_no_friday()

if __name__ == "__main__":
    main()