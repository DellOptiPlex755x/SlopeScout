# File: functions/main.py
import firebase_admin
from firebase_admin import firestore
from firebase_functions import scheduler_fn, options

import pyResort # Your updated pyResort.py (pyResort_single_collection_v5)

options.set_global_options(region="us-central1") # Ensure this matches your Firestore region

@scheduler_fn.on_schedule(
    schedule="every 5 minutes",
    timezone=scheduler_fn.Timezone("America/Los_Angeles"),
    timeout_sec=300,
    memory=options.MemoryOption.MB_256
)
def update_resort_data_in_firestore(event: scheduler_fn.ScheduledEvent) -> None:
    if not firebase_admin._apps:
        firebase_admin.initialize_app()

    print("Function triggered by schedule to update 'resort_conditions' collection.")

    # Get the structured data from pyResort
    # Expected format: {"doc_id_1": data, "doc_id_2": data, ...}
    all_documents_data = pyResort.get_all_resorts_data_for_firestore()

    if not all_documents_data:
        print("No data received from pyResort.get_all_resorts_data_for_firestore(). Exiting function.")
        return

    db = firestore.client()
    collection_name = "resort_conditions" # Target the single collection
    print(f"Received data. Updating Firestore collection: {collection_name}...")

    for document_id, document_data in all_documents_data.items():
        if document_data: # Ensure there's actual data to write
            try:
                # Construct the document reference using the collection name and document ID
                doc_ref = db.collection(collection_name).document(document_id)
                doc_ref.set(document_data, merge=True) # merge=True is good practice
                print(f"  Successfully updated Firestore for: {collection_name}/{document_id}")
            except Exception as e:
                print(f"  Error writing to Firestore for {collection_name}/{document_id}: {e}")
        else:
            print(f"  Skipping Firestore write for {document_id} in {collection_name} due to missing data.")

    print(f"Finished update_resort_data_in_firestore for '{collection_name}' execution.")

# --- Optional: HTTPs function for manual triggering ---
# from firebase_functions import https_fn
# from datetime import datetime
#
# @https_fn.on_request(region="us-central1")
# def manually_trigger_data_update(req: https_fn.Request) -> https_fn.Response:
#     if not firebase_admin._apps:
#         firebase_admin.initialize_app()
#     print("Manual trigger received for update_resort_data_in_firestore (single collection).")
#     dummy_event = scheduler_fn.ScheduledEvent(
#         job_name="manual_trigger_single_collection",
#         schedule_time=datetime.now().isoformat() + "Z",
#         timezone="UTC"
#     )
#     update_resort_data_in_firestore(dummy_event)
#     return https_fn.Response(f"Resort data update process (single 'resort_conditions' collection) triggered manually at {datetime.now()}", status=200)

