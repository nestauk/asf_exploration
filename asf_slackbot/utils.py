import datetime 
from datetime import date
from datetime import datetime as dt

def find_date_for_next_weekday(weekday):

    today = date.today()

    weekday_dict = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    weekday_nr = weekday_dict[weekday]

    days_ahead = weekday_nr - today.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7

    return today + datetime.timedelta(days_ahead)



def get_timestamp(selected_date, selected_time):

    scheduled_datetime = dt.strptime(
        selected_date + " " + selected_time, "%Y-%m-%d %H:%M"
    )

    return int(scheduled_datetime.timestamp())


def get_first_name(client, id):

    user_name = get_user_name(client, id)

    first_name = user_name.split(' ')[0]
    return first_name

def get_user_name(client, id):
    userinfo = client.users_info(
        user=id
    )

    user_name = userinfo['user']['profile']['display_name']
    return user_name