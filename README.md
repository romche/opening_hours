# opening_hours

## Part 1
### Instruction to test and run
- clone repo
- cd opening_hours
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- run test: ./manage.py test
- run api: ./manage.py runserver 0:8000
- navigate: http://localhost:8000/api/v1/hours/
- add json and post it

#### sample input json (can be copied from url above):
{
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


## Part 2
I guess format is fine, I am just wondering (hypothetical thought) how input 
json would look like if restaurant let say open 24 hours on Saturday. Plus if
day missing, does it mean that restaurant close (same as empty list) or open 24
hours or maybe user just forgot to submit it.
