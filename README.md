# Fuel Optimizer

## Fuel Optimization API

### Overview

This API, built with Django, is designed to calculate the best fuel stops along a driving route. It utilizes real-time fuel price data from a CSV file and integrates with a mapping service (such as Mapbox) to determine the driving route between two locations within the United States. The API provides a route map, recommends fuel stops based on the best fuel prices, and calculates the total fuel cost for the journey.

### Features

- Identifies optimal fuel stops along the route based on price.
- Handles routes that exceed 500 miles by including multiple fuel stops.
- Calculates total fuel costs based on a vehicle’s efficiency of 10 miles per gallon.
- Uses up-to-date fuel prices from a CSV dataset.
- Integrates with Mapbox (or similar mapping API) to fetch route information.

### Requirements

- Python 3.8+
- Django 3.2.23
- Django REST Framework
- Pandas
- Requests

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

---

