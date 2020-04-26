def leap_year(year):
    flag = False
    if (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0):
        flag = True
    return flag

def time_to_iso(time):
    year = int(time / 31556926)
    year = year + 1970
    count_leap = 0
    for i in range(1970, year+1):
        if leap_year(i):
            count_leap = count_leap + 1
    days_to_count = int(time / 86400)
    days = (time / 86400)
    days = int(days)
    days = days - count_leap
    if (leap_year(year)):
        days_since_year_started = round(days % 365) + 1
    else:
        days_since_year_started = round(days % 365)
    days_in_month_leap_year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_in_month_year = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    count_month = 1
    if (leap_year(year)):
        for i in days_in_month_leap_year:
            if days_since_year_started > i:
                days_since_year_started = days_since_year_started - i
                count_month = count_month + 1
            else:
                day = days_since_year_started + 1
                break
    else:
        for i in days_in_month_year:
            if days_since_year_started > i:
                days_since_year_started = days_since_year_started - i
                count_month = count_month + 1
            else:
                day = days_since_year_started + 1
                break
    month = count_month
    d = days_to_count * 86400
    sec = time - d
    hours = sec/3600
    hours = int(hours)
    minutes = sec - (hours*3600)
    minutes_to_print = int (minutes / 60)
    seconds = int(minutes - (minutes_to_print*60))
    date = str('{:02}-{:02}-{:02}T-{:02}-{:02}-{:02}+00'.format(year, month, day, hours, minutes_to_print, seconds))
    return date