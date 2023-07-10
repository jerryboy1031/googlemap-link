import googlemaps # get_google_maps_link(), get_distance()
import requests # load_static_map_image()
import json # load_static_map_image()
# Replace 'YOUR_API_KEY' with your actual API key



def get_google_maps_link(location_name,api_key):
    #google map api key
    gmaps = googlemaps.Client(key=api_key)
    # Geocode the location to get the coordinates 
    geocode_result = gmaps.geocode(location_name)

    if geocode_result:
        # Extract the latitude and longitude
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']

        # Generate the Google Maps link
        maps_link = f"https://www.google.com/maps?q={lat},{lng}"
        return maps_link
    else:
        return "Location not found1."

#Route distance, on the other hand, will return the distance along a route
def get_distance(location1, location2,api_key):
    #google map api key
    gmaps = googlemaps.Client(key=api_key)
    
    # Geocode the locations to get the coordinates
    geocode_result1 = gmaps.geocode(location1)
    geocode_result2 = gmaps.geocode(location2)
    
    if geocode_result1 and geocode_result2:
        # Extract the latitude and longitude for both locations
        lat1 = geocode_result1[0]['geometry']['location']['lat']
        lng1 = geocode_result1[0]['geometry']['location']['lng']
        lat2 = geocode_result2[0]['geometry']['location']['lat']
        lng2 = geocode_result2[0]['geometry']['location']['lng']

        # Calculate the distance between the locations
        distance_result = gmaps.distance_matrix((lat1, lng1), (lat2, lng2), units='metric')

        if distance_result['status'] == 'OK':
            distance = distance_result['rows'][0]['elements'][0]['distance']['text']
            return distance # (km) unit
        else:
            return "Location not found2."
    else:
        return "Location not found2."


def load_static_map_image(location,api_key):
    # Encode the location name for URL
    encoded_location = requests.utils.quote(location)
    #Maps Static API key
    zoom_var = 12  # Zoom level of the map (1-21)
    size_var = "600x400"  # Size of the image in pixels (width x height) 1x1~640x640
    # Construct the URL for the Maps Static API
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={encoded_location}&zoom={zoom_var}&size={size_var}&key={api_key}"
    print(url)
    
    try:
        # Send a GET request to retrieve the image
        response = requests.get(url)
        response.raise_for_status()  # raises exception when not a 2xx response
        #print("\n headers:",response.headers)
        
        # Check if the request was successful
        #try:
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            if data['status'] == 'OK':
                # Extract the place details
                place = data['candidates'][0] # contains various details about the place, such as its name, address, opening hours, and price level  
            else:
                print("Failed to retrieve data.")       
        else:
            return "Fail!!"
        #except json.JSONDecodeError:
         #   print("Invalid JSON response.")       
    except requests.exceptions.RequestException as e:
        # An error occurred during the request, handle the exception
        print("Error:", e)


def get_place_id(location,api_key):
    # Construct the URL for the Place Autocomplete API
    base_url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    parameters = {
        "input": location,
        "key": api_key
    }

    # Send a GET request to the API
    response = requests.get(base_url, params=parameters)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        if data['status'] == 'OK' and len(data['predictions']) > 0:
            # Extract the place ID
            place_id = data['predictions'][0]['place_id']
            return place_id
        else:
            print("No place ID found for the location.")
    else:
        print("Failed to retrieve data.")
    
    return None




def get_spot_details(location,api_key):
    place_id= get_place_id(location,api_key)
    fields = "name,rating,formatted_address,opening_hours,photos"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={api_key}"
    
    payload={}
    headers = {}
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        if data['status'] == 'OK':
            # Extract the spot details
            spot = data["result"]
            print(spot)
            # attributes--------------
            name = spot['name']
            address = spot['formatted_address']
            opening_hours = spot['opening_hours']['weekday_text']
            rating = spot.get('rating')
            photos = spot.get('photos')

            # Display the information--------
            print("Spot:", name)
            print("Address:", address)
            # opening hour
            for opening_time in opening_hours:
                print(opening_time)
                #print(opening_time.encode('ascii', 'ignore').decode('ascii'))
                
            #rating
            if rating is not None:
                print("Rating:", rating)
            else:
                print("No rating")
            #photo
            if photos is not None:
                # Retrieve the photo reference and construct the photo URL
                photo_reference = photos[0]['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                print("Photo URL:", photo_url)

            else:
                print("No photo available.")
        else:
            print("Error:", data['status'])
    else:
        print("Failed to retrieve data.")

if __name__=='__main__':
    api_key= "AIzaSyC0yOIiqV9s58sqwBNgbh_73mTUwSBtxag" # general key
    #load_static_map_image("New York,NY", api_key)
    #print(get_google_maps_link("New York, NY","AIzaSyC0yOIiqV9s58sqwBNgbh_73mTUwSBtxag"))
    #print(get_distance("桃園火車站", "新竹火車站",api_key))
    #get_spot_details("Taipei 101",api_key)
