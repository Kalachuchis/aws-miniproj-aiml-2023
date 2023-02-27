import json
import uuid
import logging
import boto3

from Employee import Employee


dynamodb_client = boto3.client("dynamodb")
s3_client = boto3.client("s3")

log = logging.getLogger()
log.setLevel(logging.INFO)


def lambda_function(event, context):
    """
    Handles employee data can return employee informations
    """
    # event_copy = event.copy()

    log.info(event)

    employee = Employee(**event)
    print(employee.__dict__)



if __name__ == "__main__":

    event = {
        "first_name": "John",
        "last_name": "Doe",
        "employee_number": uuid.uuid4().hex,
        "position": "SE2",
        "db_name": "galang-project",
    }
    context = {}
    lambda_function(event, context)
