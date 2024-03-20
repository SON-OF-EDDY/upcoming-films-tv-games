import datetime

def get_current_date():

    today = datetime.date.today()

    return str(today)

def get_current_year():

    this_year = datetime.date.today().year

    return str(this_year)