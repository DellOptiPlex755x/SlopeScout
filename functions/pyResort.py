# File: C:\Users\VS Code\Documents\GitHub\SlopeScout\functions\pyResort.py
import requests
from datetime import datetime

def get_resort_data_for_firestore(resort_name="Snow Valley"):
    """
    Fetches lift statuses and other relevant data for the specified resort
    and returns it as a dictionary.
    """
    url = "https://mtnpowder.com/feed/v3.json?bearer_token=5pGMqUcRBEG4kmDJyHBPJA9kcynwUrQoGKDxlOLfVdQ&resortId%5B%5D=173&resortId%5B%5D=58&resortId%5B%5D=57"
    resort_output = {
        "name": resort_name,
        "lifts": [],
        "weather": {},
        "last_updated": datetime.now().isoformat()
    }

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        target_resort_data = None
        for r_data in data.get('Resorts', []):
            if resort_name == r_data.get('Name', ''):
                target_resort_data = r_data
                break

        if not target_resort_data:
            print(f"{resort_name} resort not found in the API data.")
            return None

        current_conditions_base = target_resort_data.get('CurrentConditions', {}).get('Base', {})
        if current_conditions_base:
            resort_output["weather"] = {
                "temperature_f": current_conditions_base.get('TemperatureF'),
                "conditions": current_conditions_base.get('Conditions'),
            }

        target_area_data = None
        for area in target_resort_data.get('MountainAreas', []):
            if area.get('Name') == resort_name:
                target_area_data = area
                break

        if target_area_data:
            lifts_data = target_area_data.get('Lifts', [])
            if lifts_data:
                def lift_sort_key(lift):
                    name = lift.get('Name', '')
                    if name.startswith('Chair '):
                        try: return (0, int(name.replace('Chair ', '')))
                        except ValueError: pass
                    elif name.startswith('MC '):
                        try: return (2, int(name.replace('MC ', '')))
                        except ValueError: pass
                    return (1, name)

                lifts_sorted = sorted(lifts_data, key=lift_sort_key)

                for lift in lifts_sorted:
                    resort_output["lifts"].append({
                        "name": lift.get('Name', 'Unknown Lift'),
                        "status": lift.get('Status', 'Unknown'),
                        "type": lift.get('LiftType', '')
                    })
        else:
            print(f"{resort_name} mountain area not found for lifts in API data.")

        return resort_output

    except requests.exceptions.RequestException as e:
        print(f"API Request Error for {resort_name}: {e}")
        return None
    except Exception as e:
        print(f"Error processing data for {resort_name}: {e}")
        return None

def get_all_resorts_data_for_firestore():
    """
    Gets data for all specified resorts and returns a dictionary,
    keyed by a Firestore-friendly resort ID.
    """
    resorts_to_fetch = ["Snow Valley", "Snow Summit", "Bear Mountain"]
    all_data = {}
    for resort_name in resorts_to_fetch:
        data = get_resort_data_for_firestore(resort_name)
        if data:
            resort_id = resort_name.lower().replace(" ", "-")
            all_data[resort_id] = data
    return all_data

# Optional: For testing pyResort.py directly
# if __name__ == "__main__":
#     all_mountain_data = get_all_resorts_data_for_firestore()
#     if all_mountain_data:
#         import json
#         print(json.dumps(all_mountain_data, indent=2))
#     else:
#         print("No data retrieved.")