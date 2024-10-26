import math
import pandas as pd
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

# Constants from settings
API_KEY = settings.MAPBOX_API_KEY
FUEL_EFFICIENCY_MPG = settings.FUEL_EFFICIENCY
MAX_RANGE_MILES = settings.MAX_RANGE


# Load fuel prices from CSV file
def fetch_fuel_prices():
    csv_file_path = f"{settings.BASE_DIR}/fuel_prices/fuel-prices-for-be-assessment.csv"
    fuel_data = pd.read_csv(csv_file_path)

    # Clean and standardize column names
    fuel_data.columns = fuel_data.columns.str.strip()

    # Standardize the fuel price column name
    if 'Retail Price' in fuel_data.columns:
        fuel_data.rename(columns={'Retail Price': 'price'}, inplace=True)

    # Remove rows with invalid or non-numeric prices
    fuel_data = fuel_data[pd.to_numeric(fuel_data['price'], errors='coerce').notnull()]
    return fuel_data


# Call Mapbox API to get the driving route between start and end points
def fetch_route_from_mapbox(start_coords, end_coords):
    mapbox_url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_coords};{end_coords}?access_token={API_KEY}"
    response = requests.get(mapbox_url)

    if response.status_code == 200:
        return response.json()
    return None


# Calculate the optimal fuel stops along the route and the total fuel cost
def compute_fuel_stops_and_cost(route_data, fuel_data):
# def compute_fuel_stops_and_cost(fuel_data): # to test without mapbox api we can manually pass distance
    total_route_distance_miles = route_data['routes'][0]['distance'] / 1609.34  # Convert from meters to miles
    # total_route_distance_miles = 134 #manually passing distance for testing of functionality
    fuel_required_gallons = total_route_distance_miles / FUEL_EFFICIENCY_MPG
    num_fuel_stops = math.ceil(total_route_distance_miles / MAX_RANGE_MILES)

    fuel_stops_list = []
    accumulated_distance = 0
    overall_fuel_cost = 0

    for _ in range(num_fuel_stops):
        accumulated_distance += 500 if accumulated_distance + 500 < total_route_distance_miles else total_route_distance_miles - accumulated_distance

        # Find the best fuel stop based on fuel price
        optimal_stop = get_best_fuel_stop(accumulated_distance, fuel_data)

        # Compute the fuel cost for this stop
        overall_fuel_cost += optimal_stop['price'] * (MAX_RANGE_MILES / FUEL_EFFICIENCY_MPG)
        fuel_stops_list.append(optimal_stop)

    return fuel_stops_list, overall_fuel_cost


# Helper function to identify the optimal fuel stop based on price
def get_best_fuel_stop(current_distance, fuel_data):
    price_column = 'price'

    # Only sort by price, assuming distance data is unavailable in fuel_data
    print(f"Warning: 'distance' column not available in fuel data. Sorting solely by {price_column}.")
    return fuel_data.sort_values(by=price_column).iloc[0].to_dict()


# API to fetch the route and compute fuel stops and costs
@api_view(['GET'])
def route_with_fuel_stops(request):
    start_coordinates = request.GET.get('start')
    end_coordinates = request.GET.get('end')

    if not start_coordinates or not end_coordinates:
        return Response({'error': 'Start and End locations must be provided'}, status=400)

    # Fetch the driving route from Mapbox API
    route_data = fetch_route_from_mapbox(start_coordinates, end_coordinates)
    if not route_data:
        return Response({'error': 'Unable to fetch route from Mapbox API'}, status=500)

    # Load fuel price data
    fuel_data = fetch_fuel_prices()

    # Compute the fuel stops and total cost for the route
    fuel_stops_list, overall_fuel_cost = compute_fuel_stops_and_cost(route_data, fuel_data)
    # fuel_stops_list, overall_fuel_cost = compute_fuel_stops_and_cost(fuel_data)

    return Response({
        'route': route_data,
        'fuel_stops': fuel_stops_list,
        'total_cost': overall_fuel_cost
    })
