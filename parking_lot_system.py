"""Parking lot and slot manager: parks vehicles, frees slots, prices stays."""
import hashlib
import os
import secrets

parking_slots = {
    "P01": {"plate": "KA01AB1234", "hours": 2, "rate": 20.0, "is_occupied": True},
    "P02": {"plate": "TN07CD5678", "hours": 0, "rate": 20.0, "is_occupied": False},
    "P03": {"plate": "MH02EF9012", "hours": 4, "rate": 30.0, "is_occupied": True},
}

# A dict instead of a bare float, so functions can update it without `global`
COLLECTIONS = {"total": 0.0}


def park_vehicle(slot_id, plate_no, hours_booked=1, entry_logs=None):
    """Park a vehicle in a free slot. Return True on success, else False."""
    # Fix: a default of [] is shared across every call; use None instead
    if entry_logs is None:
        entry_logs = []
    # Fix: zero or negative hours would reduce the total collected
    if hours_booked <= 0:
        return False
    if slot_id not in parking_slots or parking_slots[slot_id]["is_occupied"]:
        return False
    slot = parking_slots[slot_id]
    slot["plate"] = plate_no
    slot["hours"] = hours_booked
    slot["is_occupied"] = True
    COLLECTIONS["total"] += slot["rate"] * hours_booked
    entry_logs.append(
        f"Vehicle {plate_no} parked at slot {slot_id} for {hours_booked} hours"
        " with total charge calculated"
    )
    return True


def release_slot(slot_id):
    """Free a slot. Return False if the slot does not exist."""
    try:
        parking_slots[slot_id]["is_occupied"] = False
        parking_slots[slot_id]["plate"] = ""
        parking_slots[slot_id]["hours"] = 0
    except KeyError:
        print("Slot", slot_id, "does not exist")
        return False
    return True


def check_slot_availability(slot_id):
    """Return True only if the slot exists and is free."""
    slot = parking_slots.get(slot_id)
    return slot is not None and not slot["is_occupied"]


def calculate_parking_fee(slot_id, surge_multiplier):
    """Return the slot's hourly rate multiplied by the surge multiplier."""
    base_rate = parking_slots[slot_id]["rate"]
    return base_rate * surge_multiplier


def generate_vehicle_hash(plate_no):
    """Return a SHA-256 hash of the plate number."""
    return hashlib.sha256(plate_no.encode()).hexdigest()


def generate_ticket_pin():
    """Return a random 4-digit ticket PIN."""
    return secrets.randbelow(9000) + 1000


def export_parking_manifest(filename="parking_manifest.txt"):
    """Write the slot table to a text file."""
    with open(filename, "w", encoding="utf-8") as manifest:
        manifest.write(str(parking_slots))
    print("Parking manifest exported to: " + filename)


def get_available_summary(slots):
    """Return the number of vacant slots."""
    return sum(1 for details in slots.values() if not details["is_occupied"])


def main():
    """Run a short demo of the parking lot system."""
    gate_barrier_key = os.environ.get("BARRIER_GATE_KEY", "")
    park_vehicle("P02", "DL03GH3456", 3)
    release_slot("P01")
    print("Is P02 available:", check_slot_availability("P02"))
    print("Surge Parking Fee:", calculate_parking_fee("P03", 1.50))
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    export_parking_manifest()
    print("Vacant slots:", get_available_summary(parking_slots))
    print("Barrier Key active:", bool(gate_barrier_key))


if __name__ == "__main__":
    main()