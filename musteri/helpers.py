from datetime import datetime


def get_tahsilat_shortcode(user_code):
    now = datetime.now()
    day = '{:02d}'.format(now.day)
    month = '{:02d}'.format(now.month)
    year = now.year
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    seconds = '{:02d}'.format(now.second)
    unique_name = str(day) + str(month) + str(year)[2:] + str(hour) + str(minute) + str(seconds) + user_code
    return unique_name
