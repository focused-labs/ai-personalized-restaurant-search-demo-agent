import requests

from config import MAX_NUMBER_OF_RESTAURANTS, RESTAURANT_SEARCH_RADIUS


def get_lat_lng_from_address(api_key, address):
    endpoint_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': address, 'key': api_key}
    response = requests.get(endpoint_url, params=params)
    result = response.json()
    if result['status'] != 'OK':
        raise Exception(f"ERROR: {result['status']} - Could not retrieve the latitude and/or longitude from given "
                        f"address {address}")
    location = result['results'][0]['geometry']['location']
    return location['lat'], location['lng']


def get_place_details(api_key, place_id):
    """
    Fetch detailed information for a place using Google's Place Details API.

    Parameters:
    - api_key (str): Your Google API key.
    - place_id (str): The Place ID of the desired place.

    Returns:
    - dict: Detailed place information.
    """
    endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {'place_id': place_id, 'key': api_key}
    response = requests.get(endpoint_url, params=params)
    result = response.json()
    if result['status'] != 'OK':
        raise Exception(f"ERROR: {result['status']} - Could not retrieve the place details")
    return result['result']


def find_nearby_restaurants(api_key, latitude, longitude):
    """
    Fetch nearby restaurants using Google Places API and get additional
    details using Google's Place Details API.

    Parameters:
    - api_key (str): Your Google API key.
    - latitude (float): Latitude of the user's location.
    - longitude (float): Longitude of the user's location.
    - radius (int, optional): Search within a 'radius' from the user location. Default is 500 meters.

    Returns:
    - list: List of nearby restaurants and their website.
    """
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{latitude},{longitude}",
        'radius': RESTAURANT_SEARCH_RADIUS,
        'type': 'restaurant',
        'key': api_key
    }
    response = requests.get(endpoint_url, params=params)
    results = response.json()
    if results['status'] != 'OK':
        raise Exception(f"ERROR: {results['status']} - Could not retrieve the nearby restaurants")

    restaurants = []
    for place in results['results']:
        name = place.get('name', 'Unknown Name')
        place_id = place.get('place_id', '')
        lat = place['geometry']['location']['lat'] if 'geometry' in place and 'location' in place['geometry'] else None
        lng = place['geometry']['location']['lng'] if 'geometry' in place and 'location' in place['geometry'] else None

        details = get_place_details(api_key, place_id)
        if details:
            website = details.get('website')
            restaurants.append({
                'name': name,
                'website': website,
                'latitude': lat,
                'longitude': lng
            })

        if len(restaurants) >= MAX_NUMBER_OF_RESTAURANTS:
            return restaurants
    return restaurants


def google_maps_search(api_key, address):
    """
    Unified function to retrieve nearby restaurants for a given address using Google Maps APIs.

    Parameters:
    - api_key (str): Your Google API key.
    - address (str): The address to search nearby restaurants.
    - radius (int, optional): Search within a 'radius' from the address. Default is 500 meters.

    Returns:
    - list: List of nearby restaurants and their website.
    """
    latitude, longitude = get_lat_lng_from_address(api_key, address)

    restaurants = find_nearby_restaurants(api_key, latitude, longitude)
    if not restaurants:
        return "Unable to find nearby restaurants."

    # Formulate a single string with search results
    search_results_str = "Nearby Restaurants:\n"
    for i, restaurant in enumerate(restaurants, 1):
        search_results_str += (
            f"{i}. Name: {restaurant['name']}\n"
            f"   Website: {restaurant['website']}\n"
            f"   Latitude: {restaurant['latitude']}\n"
            f"   Longitude: {restaurant['longitude']}\n"
        )

    return search_results_str.rstrip('-')
