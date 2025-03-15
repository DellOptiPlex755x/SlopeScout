# Big Bear Mountain Resorts Status Program - Lifts Only
import requests
from datetime import datetime

def get_resort_status(resort_name="Snow Valley"):
    """
    Fetches and displays lift statuses for the specified resort.

    Args:
        resort_name (str): Name of the resort to get statuses for.
                          Can be "Snow Valley", "Snow Summit", or "Bear Mountain"

    Returns:
        A formatted string with lift names and statuses.
    """
    url = "https://mtnpowder.com/feed/v3.json?bearer_token=5pGMqUcRBEG4kmDJyHBPJA9kcynwUrQoGKDxlOLfVdQ&resortId%5B%5D=173&resortId%5B%5D=58&resortId%5B%5D=57"

    try:
        # Get data from API
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Find the specified resort
        target_resort = None
        for resort in data.get('Resorts', []):
            if resort_name == resort.get('Name', ''):
                target_resort = resort
                break

        if not target_resort:
            return f"{resort_name} resort not found in the data."

        # Find the mountain area matching the resort name
        mountain_areas = target_resort.get('MountainAreas', [])
        target_area = None

        for area in mountain_areas:
            if area.get('Name') == resort_name:
                target_area = area
                break

        if not target_area:
            return f"{resort_name} mountain area not found."

        # Build the result string
        result = f"\n{resort_name.upper()}\n"
        result += "=" * 95 + "\n\n"

        # Add weather info if available
        if target_resort.get('CurrentConditions', {}).get('Base', {}).get('TemperatureF'):
            temp = target_resort.get('CurrentConditions', {}).get('Base', {}).get('TemperatureF')
            conditions = target_resort.get('CurrentConditions', {}).get('Base', {}).get('Conditions', 'Unknown')
            result += f"Current conditions: {temp}°F, {conditions}\n\n"

        # Get and format lift information
        lifts = target_area.get('Lifts', [])
        if lifts:
            result += "LIFTS:\n"
            result += "-" * 95 + "\n"

            # Sort lifts
            def lift_sort_key(lift):
                name = lift.get('Name', '')
                if name.startswith('Chair '):
                    try:
                        return (0, int(name.replace('Chair ', '')))
                    except ValueError:
                        pass
                elif name.startswith('MC '):
                    try:
                        return (2, int(name.replace('MC ', '')))
                    except ValueError:
                        pass
                return (1, name)

            lifts_sorted = sorted(lifts, key=lift_sort_key)

            # Display each lift on its own line
            for lift in lifts_sorted:
                name = lift.get('Name', 'Unknown')
                status = lift.get('Status', 'Unknown')
                lift_type = lift.get('LiftType', '')

                lift_display = f"{name} ({lift_type})"
                result += f"{lift_display:<40} {status}\n"
        else:
            result += "\nNo lift data available.\n"

        return result

    except requests.exceptions.RequestException as e:
        return f"Error connecting to the API: {e}"
    except Exception as e:
        return f"Error processing data: {e}"

def get_all_resort_statuses():
    """
    Gets lift statuses for all resorts and combines them into one report.
    """
    resorts = ["Snow Valley", "Snow Summit", "Bear Mountain"]
    result = "BIG BEAR MOUNTAIN RESORTS - STATUS REPORT\n"
    result += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    result += "=" * 95 + "\n"

    for resort in resorts:
        resort_status = get_resort_status(resort)
        result += resort_status

    return result

# Main program logic
if __name__ == "__main__":
    # Print information for all three resorts
    print(get_all_resort_statuses())