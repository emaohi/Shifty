import datetime


def make_data(n):
    data = {}
    for i in range(n):
        data['employee_%s_firstName' % i] = 'Roni'
        data['employee_%s_lastName' % i] = 'L' + str(i)
        data['employee_%s_email' % i] = 'emaohi@gmail.com'
        data['employee_%s_role' % i] = 'WA'
        data['employee_%s_dateJoined' % i] = datetime.date.today()
    data['dummy'] = 'dummy'

    return data
