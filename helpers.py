import re
from datetime import datetime
import json


def extract_json_from_reply(reply: str):
    match = re.search(r"\{[\s\S]*\}", reply)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None
    return None


def data_parse_from_chat(data: dict, intent: str, channel: str, contact_info: str) -> dict:
    """
    Parses the data dictionary to extract relevant fields for storage.
    Returns a dictionary with the parsed data.
    """
    if intent == "PRIVATE_PAY":
        parsed_data = {
            "channel": channel,
            "contact_info": contact_info,
            "patient_name": data.get("patient_name", ""),
            "weight": data.get("weight", ""),
            "pickup_address": data.get("pickup_address", ""),
            "drop_off_address": data.get("dropoff_address", ""),
            "appointment_date": data.get("appointment_date", ""),
            "one_way_or_round_trip": data.get("one_way_or_round_trip", ""),
            "equipment_needed": data.get("equipment_needed", ""),
            "any_stairs_and_accompanying_passengers": data.get(
                "any_stairs_and_accompanying_passengers", ""
            ),
            "user_name": data.get("user_name", ""),
            "phone_number": data.get("phone_number", ""),
            "email": data.get("email", ""),
            "update_time": datetime.now().isoformat(),
            "status": "completed",
        }
    elif intent == "INSURANCE_CASE_MANAGERS":
        parsed_data = {
            "channel": channel,
            "contact_info": contact_info,
            "patient_name": data.get("patient_name", ""),
            "pickup_address": data.get("pickup_address", ""),
            "drop_off_address": data.get("dropoff_address", ""),
            "authorization_number": data.get("authorization_number", ""),
            "appointment_date": data.get("appointment_date", ""),
            "update_time": datetime.now().isoformat(),
            "status": "completed",
        }
    elif intent == "DISCHARGE":
        parsed_data = {
            "channel": channel,
            "contact_info": contact_info,
            "patient_name": data.get("patient_name", ""),
            "pickup_facility_name": data.get("pickup_facility_name", ""),
            "pickup_facility_address": data.get("pickup_facility_address", ""),
            "pickup_facility_room_number": data.get("pickup_facility_room_number", ""),
            "drop_off_facility_name": data.get("dropoff_facility_name", ""),
            "drop_off_facility_address": data.get("dropoff_facility_address", ""),
            "drop_off_facility_room_number": data.get(
                "dropoff_facility_room_number", ""
            ),
            "appointment_date": data.get("appointment_date", ""),
            "is_oxygen_needed": data.get("is_oxygen_needed", ""),
            "oxygen_amount": data.get("oxygen_amount", ""),
            "is_infectious_disease": data.get("is_infectious_disease", ""),
            "weight": data.get("weight", ""),
            "update_time": datetime.now().isoformat(),
            "status": "completed",
        }
    print("parsed_data:", parsed_data)
    return parsed_data
