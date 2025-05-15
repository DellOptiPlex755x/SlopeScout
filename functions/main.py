# File: C:\Users\VS Code\Documents\GitHub\SlopeScout\functions\main.py
import firebase_admin
from firebase_admin import firestore

from firebase_functions import scheduler_fn, options
import pyResort # This will now correctly import your actual resort parsing logic

options.set_global_options(region="us-central1") # ADJUST IF NEEDED (e.g., to match your Firestore region)

@scheduler_fn.on_schedule(
    schedule="every 5 minutes",
    timezone=scheduler_fn.Timezone("America/Los_Angeles"), # Correct for Orange County
    timeout_sec=300,
    memory=options.MemoryOption.MB_256
)
def update_resort_data_in_firestore(event: scheduler_fn.ScheduledEvent) -> None:
    # Defensively ensure Firebase Admin is initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app()

    print(f"Function triggered by schedule.")
    # Safely try to access common attributes from the event object
    job_name = getattr(event, 'job_name', 'N/A')
    schedule_time = getattr(event, 'schedule_time', 'N/A')
    event_timezone = getattr(event, 'timezone', 'N/A (using function default)')

    print(f"Job Name: {job_name}")
    print(f"Schedule Time: {schedule_time}")
    print(f"Configured Timezone for event (from decorator): {event_timezone}")
    print("Attempting to fetch all resort data...")

    all_resorts_data = pyResort.get_all_resorts_data_for_firestore() # This should now work

    if not all_resorts_data:
        print("No data received from pyResort.get_all_resorts_data_for_firestore(). Exiting function.")
        return

    db = firestore.client()

    print(f"Received data for {len(all_resorts_data)} resorts. Updating Firestore...")
    for resort_id, resort_data in all_resorts_data.items():
        if resort_data:
            try:
                doc_ref = db.collection("resort_conditions").document(resort_id)
                doc_ref.set(resort_data, merge=True)
                print(f"Successfully updated Firestore for: {resort_id}")
            except Exception as e:
                print(f"Error writing to Firestore for {resort_id}: {e}")
        else:
            print(f"Skipping Firestore write for {resort_id} due to missing data in the fetched structure.")

    print("Finished update_resort_data_in_firestore execution.")

# --- Optional: HTTPs function for manual triggering ---
# (Keep commented out unless you specifically want to deploy and use it)
# from firebase_functions import https_fn
# from datetime import datetime
#
# @https_fn.on_request(region="us-central1") # Ensure region matches
# def manually_trigger_data_update(req: https_fn.Request) -> https_fn.Response:
# if not firebase_admin._apps:
# firebase_admin.initialize_app()
#     print("Manual trigger received for update_resort_data_in_firestore.")
#     dummy_event = scheduler_fn.ScheduledEvent( # Create a dummy event object
#         job_name="manual_trigger",
#         schedule_time=datetime.now().isoformat() + "Z",
#         timezone="UTC"
#     )
#     update_resort_data_in_firestore(dummy_event)
#     return https_fn.Response(f"Resort data update process triggered manually at {datetime.now()}", status=200)