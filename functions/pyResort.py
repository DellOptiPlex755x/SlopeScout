# File: functions/pyResort.py
import requests
from datetime import datetime
import traceback # For detailed error logging

# --- START: Define Custom Order for Mammoth Lifts ---
MAIN_LODGE_ORDER = [
    "Broadway Express 1", "Stump Alley Express 2", "Face Lift Express 3",
    "Unbound Express 6", "Gold Rush Express 10", "Discovery Express 11",
    "Chair 12", "Chair 13", "Chair 14", "Chair 23",
    "Panorama Lower", "Panorama Upper"
]

CANYON_LODGE_ORDER = [
    "Roller Coaster Express 4", "High 5 Express", "Chair 7", "Chair 8",
    "Canyon Express 16", "Schoolyard Express 17", "Chair 20",
    "Chair 21", "Chair 22", "Village Gondola"
]

EAGLE_LODGE_ORDER = [
    "Cloud Nine Express 9", "Eagle Express 15", "Chair 25"
]

MAMMOTH_LIFT_ORDERS = {
    "Main Lodge": MAIN_LODGE_ORDER,
    "Canyon Lodge": CANYON_LODGE_ORDER,
    "Eagle Lodge": EAGLE_LODGE_ORDER
}
# --- END: Define Custom Order for Mammoth Lifts ---

MAMMOTH_LODGES_AND_CHAIRS = {
    "Main Lodge": set(MAIN_LODGE_ORDER),
    "Canyon Lodge": set(CANYON_LODGE_ORDER),
    "Eagle Lodge": set(EAGLE_LODGE_ORDER)
}

LIFT_TYPE_OCCUPANCY = {
    "High-Speed 6 Chair": 6, "6 Chair": 6, "High-Speed Quad": 4,
    "Quad Chair": 4, "Triple Chair": 3, "Double": 2, "Gondola": 6,
    "Magic Carpet": 0
}

BIGBEAR_API_URL = "https://mtnpowder.com/feed/v3.json?bearer_token=5pGMqUcRBEG4kmDJyHBPJA9kcynwUrQoGKDxlOLfVdQ&resortId%5B%5D=173&resortId%5B%5D=58&resortId%5B%5D=57"
MAMMOTH_API_URL = "https://mtnpowder.com/feed/v3.json?bearer_token=J3UPpMHLH8kcnMvn2GrdCqhQZNBqOplx8lN-6goKyqE&resortId%5B%5D=60"

def get_lodge_or_resort_details(item_name_to_fetch):
    output_data = {
        "name": item_name_to_fetch,
        "lifts": [],
        "weather": {},
        "last_updated": datetime.now().isoformat()
    }
    current_api_url = ""
    is_mammoth_lodge_type = False

    if item_name_to_fetch in MAMMOTH_LODGES_AND_CHAIRS:
        current_api_url = MAMMOTH_API_URL
        is_mammoth_lodge_type = True
    elif item_name_to_fetch in ["Snow Valley", "Snow Summit", "Bear Mountain"]:
        current_api_url = BIGBEAR_API_URL
    else:
        print(f"Error: Unknown resort/lodge name '{item_name_to_fetch}'.")
        return None

    try:
        response = requests.get(current_api_url, timeout=15)
        response.raise_for_status()
        api_data_root = response.json()
        source_resort_json_data = None

        if is_mammoth_lodge_type:
            for r_data_item in api_data_root.get('Resorts', []):
                if r_data_item.get('Name') == "Mammoth Mountain":
                    source_resort_json_data = r_data_item
                    break
            if not source_resort_json_data:
                print(f"'Mammoth Mountain' data not found for lodge '{item_name_to_fetch}'.")
                return None
        else:
            for r_data_item in api_data_root.get('Resorts', []):
                if r_data_item.get('Name') == item_name_to_fetch:
                    source_resort_json_data = r_data_item
                    break
            if not source_resort_json_data:
                print(f"Data for '{item_name_to_fetch}' not found in API.")
                return None

        current_conditions_base = source_resort_json_data.get('CurrentConditions', {}).get('Base', {})
        if current_conditions_base:
            output_data["weather"] = {
                "temperature_f": current_conditions_base.get('TemperatureF'),
                "conditions": current_conditions_base.get('Conditions'),
            }

        if is_mammoth_lodge_type:
            actual_lodge_name_in_api = item_name_to_fetch
            temp_lifts_list = []
            lifts_found_for_this_lodge = False
            for mountain_area in source_resort_json_data.get('MountainAreas', []):
                if mountain_area.get('Name') == actual_lodge_name_in_api:
                    lifts_found_for_this_lodge = True
                    targeted_chairs_for_this_lodge = MAMMOTH_LODGES_AND_CHAIRS[actual_lodge_name_in_api]
                    for lift_api_obj in mountain_area.get('Lifts', []): # Iterate API lift objects
                        lift_name = lift_api_obj.get('Name')
                        if lift_name in targeted_chairs_for_this_lodge:
                            lift_type_str = lift_api_obj.get('LiftType', '')
                            occupancy = LIFT_TYPE_OCCUPANCY.get(lift_type_str, "N/A")
                            temp_lifts_list.append({
                                "name": lift_name,
                                "status": lift_api_obj.get('Status', 'Unknown'),
                                "occupancy_limit": occupancy,
                                "type": lift_type_str
                            })
                    break
            if not lifts_found_for_this_lodge:
                print(f"Warning: MountainArea for '{actual_lodge_name_in_api}' not found.")
            if item_name_to_fetch in MAMMOTH_LIFT_ORDERS:
                custom_order_list = MAMMOTH_LIFT_ORDERS[item_name_to_fetch]
                order_map = {name: i for i, name in enumerate(custom_order_list)}
                output_data["lifts"] = sorted(temp_lifts_list, key=lambda x: order_map.get(x['name'], float('inf')))
            else:
                output_data["lifts"] = sorted(temp_lifts_list, key=lambda x: x['name'])
        else: # Big Bear resort lift processing
            target_mountain_area_for_lifts = None
            for area in source_resort_json_data.get('MountainAreas', []):
                if area.get('Name') == item_name_to_fetch:
                    target_mountain_area_for_lifts = area
                    break

            processed_lifts_for_bb = [] # New list for processed lifts
            if target_mountain_area_for_lifts:
                lifts_data_from_api = target_mountain_area_for_lifts.get('Lifts', [])
                if lifts_data_from_api:
                    # First, sort the raw API lift objects
                    def lift_sort_key(api_lift_obj):
                        name = api_lift_obj.get('Name', '')
                        if name.startswith('Chair '):
                            try: return (0, int(name.replace('Chair ', '')))
                            except ValueError: pass
                        elif name.startswith('MC '):
                            try: return (2, int(name.replace('MC ', '')))
                            except ValueError: pass
                        return (1, name)

                    sorted_api_lifts = sorted(lifts_data_from_api, key=lift_sort_key)

                    # THEN, iterate and transform keys to lowercase for Firestore
                    for api_lift_obj in sorted_api_lifts:
                        processed_lifts_for_bb.append({
                            "name": api_lift_obj.get('Name', 'Unknown Lift'),
                            "status": api_lift_obj.get('Status', 'Unknown'),
                            "type": api_lift_obj.get('LiftType', '')
                        })
                    output_data["lifts"] = processed_lifts_for_bb # Assign the list with correct keys
            else:
                print(f"Warning: Lift data area for '{item_name_to_fetch}' not found.")
        return output_data
    except requests.exceptions.RequestException as e:
        print(f"API Request Error for {item_name_to_fetch}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error processing {item_name_to_fetch}: {e}")
        print(traceback.format_exc())
        return None

def get_all_resorts_data_for_firestore():
    all_documents_data = {}
    items_to_fetch = [
        "Snow Valley", "Snow Summit", "Bear Mountain",
        "Main Lodge", "Canyon Lodge", "Eagle Lodge"
    ]
    for item_name in items_to_fetch:
        print(f"Fetching data for: {item_name}...")
        item_data = get_lodge_or_resort_details(item_name)
        if item_data:
            firestore_id = item_name.lower().replace(" ", "-")
            all_documents_data[firestore_id] = item_data
        else:
            print(f"Failed to fetch or process data for {item_name}.")
            firestore_id = item_name.lower().replace(" ", "-")
            all_documents_data[firestore_id] = {
                "name": item_name, "lifts": [], "weather": {},
                "error": "Data unavailable", "last_updated": datetime.now().isoformat()
            }
    return all_documents_data

if __name__ == "__main__":
    print("Testing pyResort.py script (Big Bear key fix & custom lift ordering)...")
    all_data = get_all_resorts_data_for_firestore()
    if all_data:
        import json
        # print(json.dumps(all_data, indent=2))

        for resort_id, data_val in all_data.items():
            print(f"\n--- Data for: {resort_id} ---")
            print(f"  Name: {data_val.get('name')}")
            print(f"  Weather: {data_val.get('weather')}")
            print(f"  Last Updated: {data_val.get('last_updated')}")
            if data_val.get('error'):
                print(f"  Error: {data_val.get('error')}")
            print(f"  Lifts ({len(data_val.get('lifts', []))}):")
            for lift in data_val.get("lifts", []):
                print(f"    - {lift.get('name')} (Type: {lift.get('type')}, Status: {lift.get('status')})")
    else:
        print("\nNo data retrieved.")
    print("\nTest finished.")
