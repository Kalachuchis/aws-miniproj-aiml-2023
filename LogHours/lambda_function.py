import json
import logging

from Timetracker import transform_logs
from Timetracker import get_hours_required


log = logging.getLogger()
log.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Handles the time tracking input for the specified employees
    FLOW:
        get employee number
        get current hours?
        get hours to log
        get tasks to log
        log tasks in relation to hours logged

    """


if __name__ == "__main__":
    event = {
        "date": "25/02/2023",
        "time_in": "9:00 am",
        "time_out": "6:00 pm",
        "shift": "day",
        "bucket_name": "bootcamp-202301-iggy-bucket",
        "file_name": "Holidays.csv",
    }

    lambda_handler(event, {})
