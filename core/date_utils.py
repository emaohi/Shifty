import datetime


def get_days_range_by_week_num(week_no, year_no):
    curr_week = "%s-W%s" % (year_no, str(week_no))
    prev_week = "%s-W%s" % (year_no, str(week_no-1))
    sunday = str(datetime.datetime.strptime(prev_week + '-0', "%Y-W%W-%w").date().strftime("%d/%m/%Y"))
    saturday = str(datetime.datetime.strptime(curr_week + '-6', "%Y-W%W-%w").date().strftime("%d/%m/%Y"))

    return '%s --> %s' % (sunday, saturday)


def get_current_week_string():

    curr_year = datetime.datetime.now().year
    return get_days_range_by_week_num(get_curr_week_num(), curr_year)


def get_next_week_string():

    curr_year = datetime.datetime.now().year
    return get_days_range_by_week_num(get_next_week_num(), curr_year)


def get_next_week_num():
    week_no = datetime.date.today().isocalendar()[1] + 1

    is_sunday = True if datetime.datetime.today().weekday() == 6 else False
    return week_no if not is_sunday else week_no + 1


def get_curr_week_num():
    week_no = datetime.date.today().isocalendar()[1]

    is_sunday = True if datetime.datetime.today().weekday() == 6 else False
    return week_no if not is_sunday else week_no + 1


def get_curr_year():
    return datetime.date.today().year


def get_date(year, day, week):
    d = "%s-W%s" % (str(year), str(week))
    date = datetime.datetime.strptime(d + '-%s' % str(int(day) - 1), "%Y-W%W-%w")

    return date
