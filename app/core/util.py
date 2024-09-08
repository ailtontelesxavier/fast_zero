from datetime import datetime
import pytz

def get_data_now_for_time_zone():
    TIME_ZONE = 'America/Sao_Paulo'
    tz = pytz.timezone(TIME_ZONE)
    return datetime.now(tz)

def get_numbers(numbers):
    #re.sub('[^a-zA-Z0-9 \n\.]', '', numers)
    return re.sub('[^0-9]', '', numbers)