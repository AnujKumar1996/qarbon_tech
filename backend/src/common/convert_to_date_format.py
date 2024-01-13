from datetime import datetime

def convert_to_date_format(date_time):
    format_string = '%Y-%m-%dT%H:%M:%S.%fZ'
    parsed_date = datetime.strptime(date_time, format_string).strftime('%Y-%m-%d')
    return parsed_date