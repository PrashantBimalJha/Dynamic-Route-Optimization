from flask import Flask, request, render_template, flash
import googlemaps
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages to the frontend

# Initialize Google Maps API client (replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual API key)
gmaps = googlemaps.Client(key='key')

# Utility function to format travel time into days, hours, and minutes
def format_travel_time(minutes):
    if minutes < 60:
        return f"{int(minutes)} minutes"
    elif minutes < 1440:  # 1440 minutes = 24 hours
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{int(hours)} hours, {int(remaining_minutes)} minutes"
    else:
        days = minutes // 1440
        remaining_minutes = minutes % 1440
        hours = remaining_minutes // 60
        minutes_left = remaining_minutes % 60
        return f"{int(days)} days, {int(hours)} hours, {int(minutes_left)} minutes"

# Function to geocode location name to latitude and longitude and ensure it's in India
def geocode_location(location_name):
    try:
        geocode_result = gmaps.geocode(location_name)

        # Check if a result was returned
        if not geocode_result:
            raise ValueError(f"Could not find the location: {location_name}")

        # Extract the latitude and longitude from the geocoding result
        lat_lng = geocode_result[0]['geometry']['location']

        # Check if the location is in India
        for component in geocode_result[0]['address_components']:
            if 'country' in component['types'] and component['long_name'] != 'India':
                raise ValueError(f"The location {location_name} is not in India. Please provide an Indian location.")

        return lat_lng['lat'], lat_lng['lng']

    except Exception as e:
        raise ValueError(f"An error occurred while geocoding the location: {e}")

# Function to get real-time traffic data for different transport modes with alternative routes
def get_all_routes(start, end, mode):
    try:
        now = datetime.now()
        # Request directions with alternative routes
        directions_result = gmaps.directions(start, end, mode=mode, departure_time=now, alternatives=True, traffic_model="best_guess")
        
        # Handle the case when no directions are found
        if not directions_result:
            raise ValueError("No routes found for the provided locations.")

        # Extract routes and their respective details
        routes_info = []
        for route in directions_result:
            distance = route['legs'][0]['distance']['value'] / 1000  # Convert meters to kilometers

            # Use 'duration_in_traffic' if available (for driving mode), otherwise use 'duration'
            if mode == 'driving' and 'duration_in_traffic' in route['legs'][0]:
                travel_time = route['legs'][0]['duration_in_traffic']['value'] / 60  # Convert seconds to minutes
            else:
                travel_time = route['legs'][0]['duration']['value'] / 60  # Use 'duration' for non-driving modes

            reaching_time = now + timedelta(minutes=travel_time)

            # Extract the detailed steps (path names)
            steps = []
            for step in route['legs'][0]['steps']:
                instruction = step['html_instructions']  # This contains the turn-by-turn instructions in HTML
                steps.append(instruction)  # Append the instruction to the list of steps

            # Append route information with formatted travel time
            routes_info.append({
                'distance': distance,
                'travel_time': format_travel_time(travel_time),  # Format the travel time
                'reaching_time': reaching_time.strftime("%I:%M %p"),
                'steps': steps
            })

        return routes_info

    except Exception as e:
        raise ValueError(f"An error occurred while fetching traffic data: {e}")

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Route to get all possible routes
@app.route('/get_route', methods=['POST'])
def get_route():
    try:
        # Retrieve user input from the form
        start_location_name = request.form['start']
        end_location_name = request.form['end']
        mode = request.form['mode']  # Retrieve the selected transportation mode

        # Input validation
        if not start_location_name or not end_location_name or not mode:
            flash("Please provide start and end locations and select a mode of transportation.", "error")
            return render_template('index.html')

        # Geocode the start and end location names, ensuring they're in India
        start_lat_lng = geocode_location(start_location_name)
        end_lat_lng = geocode_location(end_location_name)

        # Get all possible routes based on the selected mode (car, bike, bus)
        routes_info = get_all_routes(start_location_name, end_location_name, mode)

        # Prepare the result string with all possible routes and path names
        result = f"Showing all possible routes for {mode.capitalize()} from {start_location_name} to {end_location_name}:<br><br>"
        for i, route in enumerate(routes_info, 1):
            result += (f"Route {i}: {route['distance']:.2f} km, "
                       f"Travel time: {route['travel_time']}, "
                       f"Reaching time: {route['reaching_time']}<br>"
                       f"Steps:<br>")
            for step in route['steps']:
                result += f"{step}<br>"

        return render_template('index.html', result=result)

    except ValueError as ve:
        # Display error messages on the webpage
        flash(str(ve), "error")
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
