from pymongo import MongoClient
from sbd_rohanbatrain.database.db import restaurant_collection

# Insert a new restaurant with a menu_ids array
def insert_restaurant(name, address, contact_number=None, start_time="09:00 AM", end_time="09:00 PM", lat=None, long=None, menu_ids=None):
    """
    Inserts a new restaurant into the restaurants collection with an array of menu_ids.
    
    Args:
        name (str): Name of the restaurant. (Required)
        address (str): Address of the restaurant. (Required)
        contact_number (str): Contact number of the restaurant. (Optional, Default: None)
        start_time (str): Opening time of the restaurant. (Optional, Default: "09:00 AM")
        end_time (str): Closing time of the restaurant. (Optional, Default: "09:00 PM")
        lat (float): Latitude of the restaurant's location. (Optional, Default: None)
        long (float): Longitude of the restaurant's location. (Optional, Default: None)
        menu_ids (list): List of menu unique IDs. (Optional, Default: None)
        
    Returns:
        None: This function does not return any value, it only inserts the data into the database.
    """
    location_data = {
        "address": address,
        "lat": lat,
        "long": long
    }

    restaurant_data = {
        "name": name,
        "contactNumber": contact_number,
        "orderTimings": {
            "start": start_time,
            "end": end_time
        },
        "location": location_data
    }

    if menu_ids:
        restaurant_data["menu_ids"] = menu_ids

    result = restaurant_collection.insert_one(restaurant_data)
    print(f"Restaurant inserted with ID: {result.inserted_id}")


# Update a restaurant by ID (excluding menu_ids append)
def update_restaurant(restaurant_id, name=None, address=None, contact_number=None, start_time=None, end_time=None, lat=None, long=None, menu_ids=None):
    """
    Updates the restaurant details by restaurant ID, excluding menu_ids append operations.
    
    Args:
        restaurant_id (str): Unique ID of the restaurant to update.
        name (str): New name of the restaurant. (Optional)
        address (str): New address of the restaurant. (Optional)
        contact_number (str): New contact number of the restaurant. (Optional)
        start_time (str): New opening time. (Optional)
        end_time (str): New closing time. (Optional)
        lat (float): New latitude. (Optional)
        long (float): New longitude. (Optional)
        menu_ids (list): New menu_ids array to replace the existing one. (Optional)
        
    Returns:
        None: This function does not return any value, it only updates the data.
    """
    update_data = {}

    if name:
        update_data["name"] = name
    if address:
        update_data["location"] = update_data.get("location", {})
        update_data["location"]["address"] = address
    if contact_number:
        update_data["contactNumber"] = contact_number
    if start_time:
        update_data["orderTimings"] = update_data.get("orderTimings", {})
        update_data["orderTimings"]["start"] = start_time
    if end_time:
        update_data["orderTimings"] = update_data.get("orderTimings", {})
        update_data["orderTimings"]["end"] = end_time
    if lat is not None:
        update_data["location"] = update_data.get("location", {})
        update_data["location"]["lat"] = lat
    if long is not None:
        update_data["location"] = update_data.get("location", {})
        update_data["location"]["long"] = long
    if menu_ids is not None:
        update_data["menu_ids"] = menu_ids

    if update_data:
        result = restaurant_collection.update_one(
            {"_id": restaurant_id},
            {"$set": update_data}
        )
        if result.modified_count > 0:
            print(f"Restaurant with ID {restaurant_id} updated successfully.")
        else:
            print(f"No changes made to restaurant with ID {restaurant_id}.")
    else:
        print("No update data provided.")


# Append new menu_ids to the restaurant's menu_ids array
def append_menu_ids(restaurant_id, new_menu_ids):
    """
    Appends new menu_ids to the restaurant's menu_ids array.
    
    Args:
        restaurant_id (str): Unique ID of the restaurant to update.
        new_menu_ids (list): List of new menu_ids to append to the existing menu_ids array.
        
    Returns:
        None: This function does not return any value, it only appends the data.
    """
    if new_menu_ids:
        result = restaurant_collection.update_one(
            {"_id": restaurant_id},
            {"$addToSet": {"menu_ids": {"$each": new_menu_ids}}}
        )
        if result.modified_count > 0:
            print(f"Menu IDs appended to restaurant with ID {restaurant_id}.")
        else:
            print(f"No menu IDs were appended to restaurant with ID {restaurant_id}.")
    else:
        print("No menu IDs provided for appending.")
