import json

from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APISimpleTestCase

from .views import (transform_user_json_to_human_readable_format,
                    DAYS_OF_WEEK,
                    rearrange_opening_hours,
                    pretify_opening_hours,
                    check_if_value_is_int_and_in_range)


# Create your tests here.
class TestViews(SimpleTestCase):
    def setUp(self):
        self.original_json = {
                "monday": [
                    {"type": "close", "value": 3600}
                ],
                "tuesday": [
                    {"type": "open", "value": 36000},
                    {"type": "close", "value": 64800}
                ],
                "wednesday": [],
                "thursday": [
                    {"type": "open", "value": 36000},
                    {"type": "close", "value": 64800}
                ],
                "friday": [
                    {"type": "open", "value": 36000}
                ],
                "saturday": [
                    {"type": "close", "value": 3600},
                    {"type": "open", "value": 36000}
                ],
                "sunday": [
                    {"type": "close", "value": 3600},
                    {"type": "open", "value": 43200},
                    {"type": "close", "value": 75600},
                    {"type": "open", "value": 80600}
                ]
            }
        self.desired_json = {
            "monday": [],
            "tuesday": [
                {"type": "open", "value": 36000},
                {"type": "close", "value": 64800}
            ],
            "wednesday": [],
            "thursday": [
                {"type": "open", "value": 36000},
                {"type": "close", "value": 64800}
            ],
            "friday": [
                {"type": "open", "value": 36000},
                {"type": "close", "value": 3600},
            ],
            "saturday": [
                {"type": "open", "value": 36000},
                {"type": "close", "value": 3600},
            ],
            "sunday": [
                {"type": "open", "value": 43200},
                {"type": "close", "value": 75600},
                {"type": "open", "value": 80600},
                {"type": "close", "value": 3600}
            ]
        }
        self.week_days = [
                'monday',
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday'
            ]

    def test_return_all_week_days(self):
        # checking if all day in week
        data = DAYS_OF_WEEK
        for day in data:
            self.assertIn(day, self.week_days)

    def test_check_rearrange_input_json_no_data(self):
        # should return empty dictionary
        response = rearrange_opening_hours()
        self.assertEqual(None, response)

    def test_return_week_days_with_params(self):
        # testing with json
        response = rearrange_opening_hours(self.original_json)
        for key in response:
            self.assertIn(key, DAYS_OF_WEEK)

    def test_pretify_opening_hours_no_args(self):
        # return defaut value if went wrong
        response = pretify_opening_hours()
        self.assertEqual('N/A - N/A', response)

    def test_pretify_opening_hours_with_args(self):
        # Testing right formating
        response = pretify_opening_hours(self.desired_json.get('tuesday'))
        self.assertEqual('10 AM - 6 PM', response)

    def test_pretify_opening_hours_with_args_bad(self):
        # Testing for bad arguments
        response = pretify_opening_hours('foobar')
        self.assertEqual('N/A - N/A', response)

    def test_pretify_opening_hours_with_args_bad_tuple(self):
        # Testing for bad arguments
        response = pretify_opening_hours('foobar')
        self.assertEqual('N/A - N/A', response)

    def test_check_if_value_is_int_and_in_range(self):
        response = check_if_value_is_int_and_in_range()
        self.assertEqual(False, response)

    def test_check_if_value_is_int_and_in_range_with_value(self):
        response = check_if_value_is_int_and_in_range(56000)
        self.assertEqual(True, response)

    def test_check_if_value_is_int_and_in_range_with_str_value(self):
        response = check_if_value_is_int_and_in_range('foo')
        self.assertEqual(False, response)

    def test_transform_user_json_to_human_readable_format_no_args(self):
        response = transform_user_json_to_human_readable_format()
        self.assertEqual({}, response)

    def test_transform_user_json_to_human_readable_format_arg(self):
        wanted_day = 'monday'
        response = transform_user_json_to_human_readable_format(
            json.dumps(self.original_json)
        )
        response_dict = response
        monday = response_dict.get(wanted_day)
        expected_monday = 'Closed'
        self.assertEqual(monday, expected_monday)

    def test_transform_user_json_to_human_readable_format_bad_args(self):
        response = transform_user_json_to_human_readable_format('foo')
        self.assertEqual({}, response)


class ApiTests(APISimpleTestCase):

    def test_get_status_code_for_get(self):
        # Ensure that we get status code 200
        url = reverse('opening_hours')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
