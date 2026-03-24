from datetime import datetime, timedelta, timezone


def convert_wmi_time(wmi_time):
    dt_str = wmi_time[:14]  # '20250219171739'
    microseconds = int(float("0." + wmi_time[15:21]) * 1_000_000)
    tz_offset_minutes = int(wmi_time[21:])

    dt = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
    dt = dt.replace(microsecond=microseconds)

    # Appliquer le fuseau horaire
    tz = timezone(timedelta(minutes=tz_offset_minutes))
    dt = dt.replace(tzinfo=tz)

    return dt