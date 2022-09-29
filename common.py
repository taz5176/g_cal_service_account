import datetime, re
from dateutil.relativedelta import relativedelta

import constants


def get_year(date_obj):
    """
    To return the year based on the datetime obj

    Args:
        date_obj (obj): datetime obj

    Returns:
        int: year of the datetime obj
    """
    return int(date_obj.strftime('%Y'))


def get_month(date_obj):
    """
    To return the month based on the datetime obj

    Args:
        date_obj (obj): datetime obj

    Returns:
        int: month of the datetime obj
    """
    return int(date_obj.strftime('%m'))


def get_day(date_obj):
    """
    To return the day based on the datetime obj

    Args:
        date_obj (obj): datetime obj

    Returns:
        int: day of the datetime obj
    """
    return int(date_obj.strftime('%d'))


def get_day_of_week(datetime_str, delta):
    """
    return day of week, eg. "Mon", "Tue", etc

    Args:
        datetime_str (string): date in string format
        delta (int): int day(s) difference from datetime_str

    Returns:
        string: date string
    """
    date_only = re.sub(constants.REG_EXP.REMOVE_TIME, '', datetime_str)
    date_obj = datetime.datetime.strptime(date_only, '%Y-%m-%d')
    date_obj += datetime.timedelta(days=delta)
    return date_obj.strftime("%a")


def get_workweek(date_obj):
    """
    To return the work week based on the date

    Args:
        date_obj (obj): datetime obj

    Returns:
        int: work week of the datetime obj
    """
    year = get_year(date_obj)
    month = get_month(date_obj)
    day = get_day(date_obj)
    return datetime.datetime(year, month, day).isocalendar().week


def get_workweek_dates(date_obj):
    """
    To return start and end dates of the work week
    based on the datetime obj

    Args:
        date_obj (obj): datetime obj

    Returns:
        tuple: tuple of start date str, end date str
    """
    workweek = get_workweek(date_obj)
    year = get_year(date_obj)
    start_date = datetime.date(year, 1, 1) + relativedelta(weeks=+workweek-1) + relativedelta(days=+1)
    end_date = datetime.date(year, 1, 1) + relativedelta(weeks=+workweek)
    return start_date, end_date


def get_date_only(date_str):
    """
    return date only (no time) from date string

    Args:
        date_str (string): date in string format 
                           YYYY-MM-DDTHH:MM:SS+0800

    Returns:
        string: date in string format
                YYYY-MM-DD
    """
    return re.search(constants.REG_EXP.DATE_ONLY, date_str).group()


def get_time_only(date_str):
    """
    return date only (no time) from date string

    Args:
        date_str (string): date in string format 
                           YYYY-MM-DDTHH:MM:SS+0800

    Returns:
        string: date in string format
                HH:MM:SS
    """
    return re.search(constants.REG_EXP.TIME_ONLY, date_str).group()
    

def prepare_json_schema(date_obj):
    """
    preparing the dictionary for final work week calendar output 

    Args:
        date_obj (obj): datetime object

    Returns:
        dict: dictionary of whole week empty events
    """
    start_date, _ = get_workweek_dates(date_obj)
    daily_events = {
        "Sun": {
            "date": datetime.date.strftime(start_date, '%Y-%m-%d'),
            "events": []
        },
        "Mon": {
            "date": datetime.date.strftime(start_date+datetime.timedelta(days=1), '%Y-%m-%d'),
            "events": []
        },
        "Tue": {
            "date": datetime.date.strftime(start_date+datetime.timedelta(days=2), '%Y-%m-%d'),
            "events": []
        },
        "Wed": {
            "date": datetime.date.strftime(start_date+datetime.timedelta(days=3), '%Y-%m-%d'),
            "events": []
        },
        "Thu": {
            "date": datetime.date.strftime(start_date+datetime.timedelta(days=4), '%Y-%m-%d'),
            "events": []
        },
        "Fri": {
            "date": datetime.date.strftime(start_date+datetime.timedelta(days=5), '%Y-%m-%d'),
            "events": []
        },
        "Sat": {
            "date": datetime.date.strftime(start_date+datetime.timedelta(days=6), '%Y-%m-%d'),
            "events": []
        }
    }
    return daily_events


def is_multidays_event(event):
    """
    return no. of day the event span across

    Args:
        event (object): single google event

    Returns:
        int: no of days the event span across
    """
    if 'date' in event['start']:
        start_str = event['start']['date']
        end_str = event['end']['date']
    else:
        start_str = get_date_only(event['start']['dateTime'])
        end_str = get_date_only(event['end']['dateTime'])

    delta = datetime.datetime.strptime(end_str, '%Y-%m-%d') - \
        datetime.datetime.strptime(start_str, '%Y-%m-%d')
    return delta.days
