from datetime import datetime
import pytz

def get_data_now_for_time_zone():
    TIME_ZONE = 'America/Sao_Paulo'
    tz = pytz.timezone(TIME_ZONE)
    return datetime.now(tz)