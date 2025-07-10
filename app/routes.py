from flask import Blueprint, render_template
import csv
import os
import random
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load environment variables from .env

api_key = os.getenv("API_KEY")


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Please head to /map to view the bus stop map."

@main.route('/map')
def map_view():
    stops = []

    file_path = os.path.join(os.path.dirname(__file__), 'stops.txt')
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop_name = row['stop_name'].lower()
            if "station" in stop_name:
                continue

            if "eglinton" in stop_name:
                if "at" in stop_name:
                    if stop_name.index("eglinton") < stop_name.index("at"):
                        stops.append({
                            'name': row['stop_name'],
                            'lat': float(row['stop_lat']),
                            'lon': float(row['stop_lon']),
                            'paired': False  # we'll use this to track pairing
                        })
                else:
                    stops.append({
                        'name': row['stop_name'],
                        'lat': float(row['stop_lat']),
                        'lon': float(row['stop_lon']),
                        'paired': False
                    })

    # Sort by longitude (left to right)
    stops.sort(key=lambda s: s['lon'])

    labeled_stops = []

    for i, stop in enumerate(stops):
        if stop['paired']:
            continue

        closest_idx = None
        closest_dist = float('inf')

        for j, candidate in enumerate(stops):
            if i == j or candidate['paired']:
                continue

            dist = abs(stop['lon'] - candidate['lon'])
            if dist < closest_dist:
                closest_dist = dist
                closest_idx = j

        if closest_idx is not None:
            other = stops[closest_idx]

            # Compare latitudes (vertical) to assign direction
            if stop['lat'] > other['lat']:
                stop['direction'] = 'westbound'
                other['direction'] = 'eastbound'
            else:
                stop['direction'] = 'eastbound'
                other['direction'] = 'westbound'

            stop['paired'] = True
            other['paired'] = True

            labeled_stops.append(stop)
            labeled_stops.append(other)
        else:
            stop['direction'] = 'null'
            labeled_stops.append(stop)

    for stop in labeled_stops:
        stop['people_waiting'] = random.randint(1, 20)

   # ✅ Write to a real .txt file (CSV-style)
    output_path = os.path.join(os.path.dirname(__file__), 'bus_stops.txt')
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        f.write("Name,Latitude,Longitude,Direction,People Waiting\n")
        for stop in labeled_stops:
            f.write(f"{stop['name']},{stop['lat']},{stop['lon']},{stop['direction']},{stop['people_waiting']}\n")


    return render_template("map.html", stops=labeled_stops, ai_commentary=response.text)

# Replace this with your actual key
genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-1.5-flash")

bus_stops_path = os.path.join(os.path.dirname(__file__), 'bus_stops.txt')
try:
    with open(bus_stops_path, "r", encoding="utf-8") as file:
        csv_data = file.read()
except UnicodeDecodeError:
    with open(bus_stops_path, "r", encoding="latin1") as file:
        csv_data = file.read()

prompt = f"""
You are a transit optimization AI for Toronto's TTC network.

Below is CSV data of stops along Eglinton Avenue. Each row contains:
Stop Name, Latitude, Longitude, Direction (eastbound or westbound), and People Waiting.

Each bus has a maximum capacity of 40 people. Be sure to mention this in your recommendations.

Your task is to:
- Recommend how many buses should be sent **eastbound** and at what intervals (in minutes) and certain stops to emphasize and avoid based on the number of people waiting.
- Do the same for the **westbound** direction
- Provide 1 general suggestion on improving rider experience and congestion handling
- Conclude with a 2 sentence explanation about how this system supports **UN SDG Goal 11: Sustainable Cities and Communities**, with a positive and inspiring tone, try to focus on the impact of what it means to have a well-functioning transit system.

Make the entire answer around 4 points long, with each point being a single sentence. Title the sections "Eastbound Recommendations", "Westbound Recommendations", "General Suggestions", and "UN SDG #11: Sustainable Community Impact".
Please do not use markdown formatting but use emojis to make the response engaging.

Here is the data:
{csv_data}
"""

response = model.generate_content(prompt)
print(response.text)