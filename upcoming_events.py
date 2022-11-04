import urllib.request
import json
from datetime import datetime, timedelta


EVENTS_API_URL = 'http://open-api.myhelsinki.fi/v1/events/'


def get_events() -> list:
    with urllib.request.urlopen(EVENTS_API_URL) as response:
        json_response = json.load(response)
        return json_response['data']


def get_date(event: dict) -> str:
    return event['event_dates']['starting_day']


def get_name(event: dict) -> str:
    names = event['name']
    return names['fi'] or names['en'] or names['sv'] or names['zh']


def filter_upcoming(events: list, days=30) -> list:
    today = datetime.utcnow()
    next_month = today + timedelta(days=days)

    selected = []
    for event in events:
        start_date = get_date(event)

        if start_date and today.isoformat() <= start_date <= next_month.isoformat():
            selected.append(event)

    return selected


def quicksort(data: list) -> list:
    if len(data) <= 1:
        return data

    pivot = data[0]
    left = []
    right = []
    middle = []
    pivot_date = get_date(pivot)

    for item in data:
        item_date = get_date(item)

        if item_date == pivot_date:
            middle.append(item)
        elif item_date < pivot_date:
            left.append(item)
        else:
            right.append(item)

    return quicksort(left) + middle + quicksort(right)


def main():
    events = get_events()
    events = filter_next_month(events)
    events = quicksort(events)

    for event in events:
        start_day = get_date(event)
        name = get_name(event)
        print(f'{start_day} {name}')


if __name__ == '__main__':
    main()