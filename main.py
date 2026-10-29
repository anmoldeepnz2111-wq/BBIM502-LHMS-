
# File: main.py
# Author: Anmoldeep Singh
# Description: Langham Hotel Management System
# Date: 29 October 2026

rooms_list = []
allocations_dict = {}


# Display the available hotel management options.
def show_menu():
    """Display the main menu options."""
    print("\n===== LANGHAM HOTEL MANAGEMENT SYSTEM =====")
    print("1. Add Room")
    print("2. Delete Room")
    print("3. Display Room Details")
    print("4. Allocate Room")
    print("5. Display Allocation Details")
    print("6. Billing and De-Allocation")
    print("7. Save Allocations to File")
    print("8. Show Allocations from File")
    print("9. Backup and Clear File")
    print("0. Exit")


def main():
    """Control the menu until the user chooses to exit."""
    while True:
        show_menu()

        try:
            choice = input("Enter your choice: ").strip()

            if choice == "0":
                print("Thank you for using Langham Hotel Management System.")
                break
            elif choice == "1":
                add_room()
            elif choice == "2":
                delete_room()
            elif choice == "3":
                display_room_details()
            elif choice == "4":
                allocate_room()
            elif choice == "5":
                display_allocation_details()
            elif choice == "6":
                billing_and_deallocation()
            elif choice == "7":
                print("Save Allocations to File selected.")
            elif choice == "8":
                print("Show Allocations from File selected.")
            elif choice == "9":
                print("Backup and Clear File selected.")
            else:
                print("Invalid choice. Please enter a number from 0 to 9.")

        except EOFError:
            print("\nNo more input available. Exiting the application.")
            break


def find_room(room_number):
    """Return the room dictionary for a room number, or None if not found."""
    for room in rooms_list:
        if room["room_number"] == room_number:
            return room
    return None
 
 
def add_room():
    room_number = input("Enter room number: ").strip()
    if room_number == "":
        print("Room number cannot be empty.")
        return
 
    if find_room(room_number) is not None:
        print("This room number already exists.")
        return
 
    room_type = input("Enter room type (Standard/Deluxe/Suite): ").strip()
    if room_type == "":
        print("Room type cannot be empty.")
        return
 
    try:
        nightly_rate = float(input("Enter nightly rate: "))
    except ValueError:
        print("Invalid nightly rate. Enter a valid number.")
        return
 
    if nightly_rate <= 0:
        print("Nightly rate must be greater than zero.")
        return
 
    room = {
        "room_number": room_number,
        "room_type": room_type,
        "nightly_rate": nightly_rate,
        "available": True,
    }
    rooms_list.append(room)
    print("Room", room_number, "added successfully.")
 
 
def delete_room():
    room_number = input("Enter room number to delete: ").strip()
    if room_number == "":
        print("Room number cannot be empty.")
        return
 
    room = find_room(room_number)
    if room is None:
        print("Room", room_number, "does not exist.")
        return
 
    if room_number in allocations_dict:
        print("Cannot delete this room because it is allocated.")
        return
 
    rooms_list.remove(room)
    print("Room", room_number, "deleted successfully.")
 
 
def display_room_details():
    if len(rooms_list) == 0:
        print("No rooms are currently available in the room list.")
        return
 
    print("\n===== ROOM DETAILS =====")
    for room in rooms_list:
        print("Room Number:", room["room_number"])
        print("Room Type:", room["room_type"])
        print("Nightly Rate: $" + format(room["nightly_rate"], ".2f"))
        if room["available"]:
            print("Status: Available")
        else:
            print("Status: Occupied")
        print("-------------------------")
 
 
def allocate_room():
    room_number = input("Enter room number to allocate: ").strip()
    if room_number == "":
        print("Room number cannot be empty.")
        return
 
    room = find_room(room_number)
    if room is None:
        print("Room", room_number, "does not exist.")
        return
 
    if not room["available"]:
        print("This room is already occupied.")
        return
 
    customer_name = input("Enter customer name: ").strip()
    if customer_name == "":
        print("Customer name cannot be empty.")
        return
 
    if not any(ch.isalpha() for ch in customer_name):
        print("Customer name must contain letters.")
        return
 
    try:
        nights = int(input("Enter number of nights: "))
    except ValueError:
        print("Invalid number of nights. Enter a whole number.")
        return
 
    if nights <= 0:
        print("Number of nights must be greater than zero.")
        return
 
    allocations_dict[room_number] = {
        "customer_name": customer_name,
        "room_type": room["room_type"],
        "nightly_rate": room["nightly_rate"],
        "number_of_nights": nights,
    }
    room["available"] = False
 
    print("Room", room_number, "allocated successfully.")
    print("Customer:", customer_name)
    print("Number of nights:", nights)
 
 
def display_allocation_details():
    if len(allocations_dict) == 0:
        print("There are no current room allocations.")
        return
 
    print("\n===== ROOM ALLOCATION DETAILS =====")
    for room_number in allocations_dict:
        booking = allocations_dict[room_number]
        charge = booking["nightly_rate"] * booking["number_of_nights"]
 
        print("Room Number:", room_number)
        print("Customer Name:", booking["customer_name"])
        print("Room Type:", booking["room_type"])
        print("Nightly Rate: $" + format(booking["nightly_rate"], ".2f"))
        print("Number of Nights:", booking["number_of_nights"])
        print("Estimated Room Charge: $" + format(charge, ".2f"))
        print("------------------------------------")
 
 
def billing_and_deallocation():
    room_number = input("Enter room number for checkout: ").strip()
    if room_number == "":
        print("Room number cannot be empty.")
        return
 
    room = find_room(room_number)
    if room is None:
        print("Room", room_number, "does not exist.")
        return
 
    if room_number not in allocations_dict:
        print("This room has no active allocation.")
        return
 
    booking = allocations_dict[room_number]
    total_bill = booking["nightly_rate"] * booking["number_of_nights"]
 
    print("\n===== GUEST BILL =====")
    print("Room Number:", room_number)
    print("Customer Name:", booking["customer_name"])
    print("Nightly Rate: $" + format(booking["nightly_rate"], ".2f"))
    print("Number of Nights:", booking["number_of_nights"])
    print("Total Bill: $" + format(total_bill, ".2f"))
 
    del allocations_dict[room_number]
    room["available"] = True
 
    print("Checkout completed successfully.")
    print("Room", room_number, "is now available.")


if __name__ == "__main__":
    main()
