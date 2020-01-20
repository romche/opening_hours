import datetime
import json
from json import JSONDecodeError
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Dummy is for example purpose only
# showing to user as an example input
DUMMY = {
    "monday": [{"type": "close", "value": 3600}],
    "tuesday": [{"type": "open", "value": 36000},
                {"type": "close", "value": 64800}],
    "wednesday": [],
    "thursday": [{"type": "open", "value": 36000},
                 {"type": "close", "value": 64800}],
    "friday": [{"type": "open", "value": 36000}],
    "saturday": [{"type": "close", "value": 3600},
                 {"type": "open", "value": 36000}],
    "sunday": [{"type": "close", "value": 3600},
               {"type": "open", "value": 43200},
               {"type": "close", "value": 75600},
               {"type": "open", "value": 80600}]
}

# We will need all days in week since we will return all
# day despite on user json input. Plus we need it to figure
# before day
DAYS_OF_WEEK = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]


def rearrange_opening_hours(opening_hours_by_day=None):
    """
    Function will rearrange json object that we got from
    user. Basically we want to move "close" object to we
    it belong.

    Args:
        opening_hours_by_day (dict): user input of restaurant opening hours

    Returns:
        rearranged_json_obj (dict): New json obj with open/close
                                    in same day even if restaurant
                                    closes on next day
    """
    # If there is no json object, then returning None
    rearranged_opening_hours_by_day = None

    # If there is object, then we can start
    if opening_hours_by_day:

        # Since we want to be sure that we have all days in week covered
        for day in DAYS_OF_WEEK:

            hours_for_day = opening_hours_by_day.get(day, [])

            # Checking if opening day have any entries
            if len(hours_for_day) > 0:

                # if first entry type is equal to close
                if hours_for_day[0].get('type') == 'close':

                    # removing from list
                    close_entry_for_move = hours_for_day.pop(0)

                    # we will be moving "type:close" entry to day before, so
                    # we need to know which day is before. Except for monday
                    # it is always index - 1
                    if day == 'monday':
                        day_before_index = -1
                    else:
                        day_before_index = DAYS_OF_WEEK.index(day) - 1

                    # get hours of day before
                    hours_of_day_before = opening_hours_by_day.get(
                        DAYS_OF_WEEK[day_before_index]
                    )
                    # adding "type_close" entry at the end
                    hours_of_day_before.append(close_entry_for_move)

        rearranged_opening_hours_by_day = opening_hours_by_day

    return rearranged_opening_hours_by_day


def check_if_value_is_int_and_in_range(value=None):
    """
    Function will check that value/object is an integer and
    it is between 0 and 86399

    Args:
        value (obj): value that we want to check

    Returns:
        True / False (bool): if int and in range then True
                             else False

    """
    value_is_ok = False
    if value:
        try:
            if 0 <= int(value) < 86400:
                value_is_ok = True
        except (TypeError, ValueError) as e:  # noqa: F841
            value_is_ok = False

    return value_is_ok


def pretify_opening_hours(open_close_time=None):
    """
    Function will format open/close hours to AM/PM, will take
    open / close tuple as parameters

    Args:
        open_close_time (tuple): open/close in seconds

    Returns:
        formated_hours (str): will return in desire format
                              e.g. '10:00 AM - 6:00 PM'

    """
    # Default if no argument
    formated_hours = 'N/A - N/A'

    if open_close_time:
        # Here we assume that first in tuple is opening time and
        # second is closing time, assuming is always bad
        try:
            raw_open_time = open_close_time[0].get('value')
            raw_close_time = open_close_time[1].get('value')

        # in except we will be returning default value
        except AttributeError as e:  # noqa: F841
            return formated_hours

        # Checking if value is in range
        if check_if_value_is_int_and_in_range(raw_open_time) \
                and check_if_value_is_int_and_in_range(raw_close_time):

            # Adding timedelta to datetime object for opening time
            open_time = \
                datetime.datetime(1970, 1, 1) + datetime.timedelta(
                    seconds=raw_open_time
                )
            # Doing same with closing time
            close_time = \
                datetime.datetime(1970, 1, 1) + datetime.timedelta(
                    seconds=raw_close_time
                )

            # Adding human friendly time to string
            formated_hours = \
                f'{open_time.strftime("%-I %p")} - {close_time.strftime("%-I %p")}'  # noqa: E501

        # If checking fails, we just pass since we have N/A already
        else:
            pass

    return formated_hours


def transform_user_json_to_human_readable_format(restaurant_hours_json=None):
    """
    Function takes json-formatted opening hours of a restaurant
    as an input and will produce more human readable json -format

    Args:
        restaurant_hours_json (json): users opening hours of a restaurant

    Returns:
        human_readable_format (dict): human readable format
    """
    # Default return value if json_obj is not passed
    human_readable_format = dict()

    # if we have user restaurant_hours_json object
    if restaurant_hours_json:

        # Try to convert user json to dict,
        # if doesn't work then skipping rest
        try:
            users_restaurant_hours = json.loads(restaurant_hours_json)
        except JSONDecodeError as e:  # noqa: F841
            users_restaurant_hours = None

        # if we have data in dict format
        if users_restaurant_hours:

            # rearrange possible type:close to where it belongs
            organised_opening_hours = rearrange_opening_hours(
                users_restaurant_hours
            )

            # iterating days and days opening hours
            for day, hours in organised_opening_hours.items():

                # if we have hours
                if len(hours) > 0:
                    # Iterating hours entries in pairs (open / close)
                    # and making them human readable
                    hours_in_specific_day = [
                        pretify_opening_hours(open_close)
                        for open_close in list(zip(hours[0::2], hours[1::2]))
                    ]
                # empty list means Closed
                else:
                    hours_in_specific_day = ['Closed']

                # joining hours if sever per day
                human_readable_format[day] = ', '.join(hours_in_specific_day)

    return human_readable_format


@api_view(['GET', 'POST'])
def opening_hours(request):
    """
    Will display restaurant opening hours in human readable format

    GET: Returns a page with an example json
    POST: Will return opening hours in human readable format

    """
    if request.method == 'POST':
        formated_data = transform_user_json_to_human_readable_format(
            json.dumps(request.data)
        )
        return Response({"message": "Succes", "data": formated_data})
    return Response(DUMMY)
