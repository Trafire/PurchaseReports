from datetime import datetime


def convert_to_datetime(date_str, date_format):
    return datetime.strptime(date_str, date_format)


def f2_to_datetime(date_str):
    date_str = date_str.replace('-','/')
    try:
        return convert_to_datetime(date_str, '%d/%m/%y')
    except(ValueError):
        return convert_to_datetime(date_str, '%d/%m/%Y')


def datetime_to_f2(date_obj):
    return date_obj.strftime('%d/%m/%y')