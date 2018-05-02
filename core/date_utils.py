import datetime


def get_days_range_by_week_num(week_no, year_no):
    curr_week = "%s-W%s" % (year_no, str(week_no))
    prev_week = "%s-W%s" % (year_no, str(week_no-1))
    sunday = str(datetime.datetime.strptime(prev_week + '-0', "%Y-W%W-%w").date().strftime("%d/%m/%Y"))
    saturday = str(datetime.datetime.strptime(curr_week + '-6', "%Y-W%W-%w").date().strftime("%d/%m/%Y"))

    return sunday, saturday


def get_current_week_string():
    return get_week_string(get_curr_week_num(), get_curr_year())


def get_next_week_string():

    return get_week_string(get_next_week_num(), get_curr_year())


def get_week_string(week, year):
    sunday, saturday = get_days_range_by_week_num(week, year)
    return __make_week_range_string(sunday, saturday)


def __make_week_range_string(first, last):
    return '%s --> %s' % (first, last)


def __convert_date_for_calendar(date):
    return date.replace('/', '-')


def get_curr_week_sunday():
    curr_sunday = get_days_range_by_week_num(get_curr_week_num(), get_curr_year())[0]
    return __convert_date_for_calendar(curr_sunday)


def get_next_week_sunday():
    next_sunday = get_days_range_by_week_num(get_next_week_num(), get_curr_year())[0]
    return __convert_date_for_calendar(next_sunday)


def get_next_week_num():
    week_no = get_today_date().isocalendar()[1] + 1

    is_sunday = True if datetime.datetime.today().weekday() == 6 else False
    return week_no if not is_sunday else week_no + 1


def get_curr_week_num():
    week_no = get_today_date().isocalendar()[1]

    is_sunday = True if datetime.datetime.today().weekday() == 6 else False
    return week_no if not is_sunday else week_no + 1


def get_curr_year():
    return get_today_date().year


def get_date(year, day, week):
    d = "%s-W%s" % (str(year), str(week))
    date = datetime.datetime.strptime(d + '-%s' % str(int(day) - 1), "%Y-W%W-%w")
    return date


def get_birth_day_from_age(age):
    return datetime.datetime.now() - datetime.timedelta(days=age*365)


def get_started_month_from_month_amount(month_cnt):
    return get_today_date() - datetime.timedelta(month_cnt*365/12)


def get_today_date():
    return datetime.date.today()


def get_today_day_num_str(origin_weekday):
    return ((origin_weekday + 1) % 7) + 1


def get_current_deadline_date_string(day_of_week):
    date = get_current_deadline_date(day_of_week)
    if date:
        return date.strftime('%Y/%m/%d')
    return None


def get_current_deadline_date(day_of_week):
    is_sunday = True if day_of_week == 1 else False
    r_date = get_date(get_curr_year(), day_of_week,
                      get_curr_week_num() if not is_sunday else get_curr_week_num() - 1)
    if r_date.date() > get_today_date():
        return r_date
    return None


def get_current_week_range():
    date = get_today_date()
    return get_week_range(date)


def get_week_range(date):
    start_week = date - datetime.timedelta((date.weekday() + 1) % 7)
    end_week = start_week + datetime.timedelta(7)

    return start_week, end_week


def get_days_hours_from_delta(td):
    return td.days, td.seconds//3600


def timestamp_now():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
