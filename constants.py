from collections import namedtuple


# tuple of regular expression for str manipulation
REG_EXP = namedtuple(
    'reg_exp', [
        'FREQ',
        'DAY',
        'DATE_ONLY',
        'REMOVE_TIME',
        'TIME_ONLY',
        'DATE_STRING_FORMAT',
        'DATETIME_STRING_FORMAT'
        ]
    )(
        '(?<=FREQ=).*(?=;)',
        '(?<=;BYDAY=).*',
        '.*(?=T)',
        '(?=T).*',
        '(?<=T).*(?=:[0-9]{2}\+)',
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S+0800'
        )
    
# tuple of datetime format
FORMAT = namedtuple(
    'reg_exp', [
        'DATE_STRING_FORMAT',
        'DATETIME_STRING_FORMAT'
        ]
    )(
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S+0800'
        )