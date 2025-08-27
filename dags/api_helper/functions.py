from datetime import datetime, timedelta

def get_time_range_as_per_sync_frequency(sync_frequency: int,buffer: int, base_time: datetime):
    # # asia_kolkata_tz = pytz.timezone('Asia/Kolkata')
    base_time = base_time - timedelta(minutes=buffer)
    # print(base_time)

    # # Step 2: Truncate to 5-minute window
    window_start_time = base_time - timedelta(minutes=sync_frequency)

    window_start_minute = (window_start_time.minute // sync_frequency)*sync_frequency - sync_frequency

    if window_start_minute < 0:
        start_time = window_start_time - timedelta(minutes=sync_frequency)
        start_time = start_time.replace(minute=60-sync_frequency, second=0, microsecond=0)

    else:
        start_time = window_start_time.replace(minute=window_start_minute, second=0, microsecond=0)

    # Step 3: Add 4 minutes 59 seconds to get end time
    end_time = start_time + timedelta(minutes=sync_frequency-1, seconds=59)

    # Step 4: Convert to strings
    start_datetime_str = start_time.strftime('%Y-%m-%dT%H:%M:%S')
    end_datetime_str = end_time.strftime('%Y-%m-%dT%H:%M:%S')

    return start_datetime_str,end_datetime_str