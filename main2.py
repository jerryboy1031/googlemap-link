import googlemaps # get_google_maps_link(), get_distance()
import requests # load_static_map_image()
import time as Time

import gspread
#the old one is deprecated: from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
#launches a browser asking you for authentication in data2sheet-1\main.py
def get_cell_val(col,row):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
    credentials= Credentials.from_service_account_file("secret_credential.json", scopes=scope) 
    client = gspread.authorize(credentials)
    sh = client.open(title='EU_tour')#,folder_id='1CCJ6d-P381whToCFP6V9rb_mkI84GuHIF6z5rqWAzzg') #error--------------
    wks= sh.worksheet("地圖用")
    print("\n value: ",wks.cell(row=row,col=col).value)
    return wks.cell(row=row,col=col).value
    

def data2sheet(data,row,col):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
    #credentials = ServiceAccountCredentials.from_json_keyfile_name(mykey_json, scope)
    credentials= Credentials.from_service_account_file("secret_credential.json", scopes=scope) 
    client = gspread.authorize(credentials)
    sh = client.open(title='EU_tour')#,folder_id='1CCJ6d-P381whToCFP6V9rb_mkI84GuHIF6z5rqWAzzg') #error--------------
    wks= sh.worksheet("地圖用")
    wks.update_acell(col+str(row), data)
    return 0


def get_placeID(location,api_key):
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
            return data['predictions'][0]['place_id']
        else:
            return "No place ID found for the location."
    else:
        return "Failed to retrieve data."


def get_place經緯(location,api_key,placeID):
    url=f"https://maps.googleapis.com/maps/api/geocode/json?place_id={placeID}&key={api_key}"
    
    # Send a GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        Time.sleep(1)
        # Parse the JSON response
        data = response.json()
        if data["status"]== 'OK':
            # extract longitude and latitude
            lng= data['results'][0]['geometry']['location']['lng']
            lat= data['results'][0]['geometry']['location']['lat']
            return lng,lat
        else:
            print("status not ok")
    else: 
        print("Invalid request")
    
def get_spot_details(location,api_key,row,placeID):
    fields = "name,formatted_address"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={placeID}&fields={fields}&key={api_key}"
    payload={}
    headers = {}
    
    response = requests.request("GET", url, headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        #Time.sleep(5)
        # Parse the JSON response
        data = response.json()
        
        if data['status'] == 'OK':
            Time.sleep(1)
            # Extract the spot details
            spot = data["result"]
            #print(spot)
            # attributes--------------
            name = spot['name']
            address = spot['formatted_address']
            
            # Display the information--------   
            return name,address
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
    lis=[22,65,66,70,62,103]
    for i in lis:
        spot='法國 '+get_cell_val(row=i,col=1)
        placeID= get_placeID(spot, api_key)
        if get_spot_details(spot,api_key,i,placeID) is not None:
            name,address=get_spot_details(spot,api_key,i,placeID) # type: ignore
            data2sheet(name,row=i,col='A')
            data2sheet(address,row=i,col='B')
        if get_place經緯(spot,api_key,placeID) is not None:
            lng,lat= get_place經緯(spot,api_key,placeID)
            data2sheet(lat,row=i,col='C')
            data2sheet(lng,row=i,col='D')
            
        
        