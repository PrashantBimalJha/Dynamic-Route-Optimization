# Dynamic Bus Route Monitoring Systems

A web application to monitor and rationalize bus routes dynamically based on real-time traffic and road conditions. It allows users to view available bus stops, check the next bus arrivals, and visualize routes and traffic information on a map.

## Features

- Display all bus stops in Delhi.
- Show the next buses arriving at a selected stop with their expected arrival times.
- Provide traffic information between specified locations.
- Visualize routes and traffic on Google Maps.
- Dynamic error handling and user-friendly interface.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API Integration**: Google Maps API
- **Hosting**: Local development server (Flask)

---

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Google Cloud account with an API key for Maps and Directions services
- Node.js (for advanced frontend development, optional)

---

## Project Setup

Follow these steps to set up the project:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/dynamic-bus-route-monitoring.git
cd dynamic-bus-route-monitoring
```

### 2. Install Dependencies

Install the required Python libraries:

```bash
pip install Flask googlemaps
```

### 3. Configure API Keys

Replace `YOUR_GOOGLE_CLOUD_API_KEY` in the following files with your actual Google Maps API key:

- `app.py`
- `index.html`
- `app.js`

### 4. Run the Application

Start the Flask server:

```bash
python app.py
```

Access the application at `http://127.0.0.1:5000`.

---

## File Structure

```
dynamic-bus-route-monitoring/
├── app.py            # Backend server script (Flask)
├── index.html        # Main HTML page
├── app.js            # JavaScript for frontend functionality
├── styles.css        # Styling for the app
├── bus_stops.json    # Bus stops data
├── README.md         # Project documentation
```

---

## Usage

1. **View Bus Stops**:
   - All bus stops in Delhi are displayed in the "Bus Stops" section.
   
2. **Check Next Bus**:
   - Enter a bus stop name and click "Fetch Next Bus Arrival" to see upcoming buses and arrival times.

3. **Traffic Information**:
   - Enter the origin and destination locations, then click "Check Traffic" to view real-time traffic conditions.

4. **Map Visualization**:
   - Routes and traffic information are dynamically displayed on Google Maps embedded in the app.

---

## Error Handling

- Provides error messages for:
  - Missing inputs (e.g., bus stop name, origin, or destination).
  - Invalid or unavailable data from the API.
- Ensures the app remains user-friendly even in case of errors.

---



## Future Enhancements

- **Real-Time Bus Tracking**: Use GPS data for dynamic updates.
- **User Authentication**: Allow users to save their favorite stops and routes.
- **Database Integration**: Store bus and traffic data for analytics.

---
