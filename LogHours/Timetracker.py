import boto3
import datetime
import pandas as pd
import numpy as np

from calendar import monthrange

dynamodb_client = boto3.client("dynamodb")
s3_client = boto3.client("s3")


def convert_time_to_ints(time_string):
    time_inputs = time_string.split(" ")
    is_afternoon = time_inputs[1].lower() == "pm"
    time = time_inputs[0].split(":")

    hour = int(time[0]) if not is_afternoon else int(time[0]) + 12
    minute = int(time[1])

    return {"hour": hour, "minute": minute}


def transform_logs(date, logged_in, logged_out, shift):
    date_parts = date.split("/")
    day = int(date_parts[0])
    month = int(date_parts[1])
    year = int(date_parts[2])

    time_in = convert_time_to_ints(logged_in)
    log_in = datetime.datetime(
        year, month, day, time_in["hour"], time_in["minute"]
    )

    time_out = convert_time_to_ints(logged_out)
    log_out = datetime.datetime(
        year, month, day, time_out["hour"], time_out["minute"]
    )
    if shift == "night":
        log_out = log_out + datetime.timedelta(days=1)

    logged_hours = ((log_out - log_in).total_seconds()) / 60**2

    return {
        "date": str(datetime.datetime(year, month, day)),
        "time_in": log_in.ctime(),
        "time_out": log_out.ctime(),
        "logged_hours": logged_hours,
    }


def get_hours_required(bucket_name, file_name, folder):
    bucket_path = f"{folder}/{file_name}"
    download_path = f"./{file_name}"
    s3_client.download_file(bucket_name, bucket_path, download_path)

    holiday_df = pd.read_csv(download_path, parse_dates=[0])
    holiday_df.rename(columns={"Unnamed: 1": "DAY"}, inplace=True)

    # getting the current month and the next month
    date_now = datetime.datetime.now()
    days_in_month = lambda dt: monthrange(dt.year, dt.month)[1]
    curr_month = date_now.replace(day=1)
    next_month = curr_month + datetime.timedelta(days_in_month(curr_month))

    # get the number of weekdays

    no_of_weekdays = np.busday_count(
        curr_month.strftime("%Y-%m"),  # formats date to YYYY-MM
        next_month.strftime("%Y-%m"),  # formats date to YYYY-MM
    )

    hours_required = no_of_weekdays * 8

    busday_holidays = holiday_df.loc[holiday_df["DATE"].dt.dayofweek < 5]

    non_working_days = busday_holidays.loc[
        busday_holidays["DATE"].dt.month == date_now.month
    ].shape[0]

    return hours_required - (non_working_days * 8)
