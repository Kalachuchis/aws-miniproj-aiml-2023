import logging
import boto3

log = logging.getLogger()
log.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")
s3_client = boto3.client("dynamodb")


def add_user(db_name, **kwargs):
    try:
        response = dynamodb_client.put_item(
            TableName=db_name,
            Item={
                "PK": {"S": f"Employee {kwargs['employee_number']}"},
                "SK": {"S": "Details"},
                "First_Name": {"S": kwargs["first_name"]},
                "Last_Name": {"S": kwargs["last_name"]},
                "User_Name": f"{(kwargs['first_name']).lower()}.{(kwargs['last_name']).lower()}",
                "Role": {"S": kwargs["role"]},
            },
        )

        return response
    except Exception as e:
        log.error(str(e))


def get_user_by_id(db_name, employee_number):
    response = dynamodb_client.get_item(
        TableName=db_name,
        Key={
            "PK": {"S": f"Employee {employee_number}"},
            "SK": {"S": "Details"},
        },
    )
    return response


def get_user_by_username(db_name, user_name):
    response = dynamodb_client.get_item(
        TableName=db_name,
        IndexName="User_Name-index",
        Key={
            "User_Name": {"S": f"Employee {user_name}"},
            "SK": {"S": "Details"},
        },
    )
    return response
