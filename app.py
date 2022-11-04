from flask import Flask, jsonify
from upcoming_events import filter_upcoming, get_events, quicksort

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, Docker!</h1>'


@app.route('/api/events')
def events_next_month():
    all_events = get_events()
    next_week = filter_upcoming(all_events, days=7)
    sorted_events = quicksort(next_week)

    return jsonify(sorted_events)