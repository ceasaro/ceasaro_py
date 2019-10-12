from datetime import datetime


def str_to_date(start_date_str):
    try:
        return datetime.strptime(start_date_str, '%d-%m-%Y')
    except ValueError:
        return datetime.strptime(start_date_str, '%Y%m%d')


