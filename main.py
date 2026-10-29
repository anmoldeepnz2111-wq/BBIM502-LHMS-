# File: main.py
# Author: Anmoldeep Singh
# Description: Langham Hotel Management System
# Date: 29 October 2026

try:
    import ast
    from datetime import datetime
except ImportError:
    print("A required module could not be found. Exiting.")
    exit()

STUDENT_ID = "850010874"  
DATA_FILE = "LHMS_" + STUDENT_ID + ".txt"
ROOM_TYPES = ["Standard", "Deluxe", "Suite"]

rooms_list = []
allocations_dict = {}


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
                save_allocations_to_file()
            elif choice == "8":
                show_allocations_from_file()
            elif choice == "9":
                backup_and_clear_file()
            else:
                print("Invalid choice. Please enter a number from 0 to 9.")

        except EOFError:
            print("\nNo more input available. Exiting the application.")
            break
        except NameError:
            print("A variable was used before it was defined.")


def find_room(room_number):
    """Return the room dictionary for a room number, or None if not found."""
    for room in rooms_list:
        if room["room_number"] == room_number:
            return room
    return None


"""
calculate_bill works out the cost of a stay.
It multiplies the nightly rate by the number of nights and then
takes off the discount percentage. If something goes wrong it
shows a message and returns None so the caller can stop safely.
"""
def calculate_bill(nightly_rate, nights, discount):
    """Return the total bill, or None if it cannot be calculated."""
    try:
        total = nightly_rate * nights
        total = total - (total * discount / 100)
        return total
    except TypeError:
        print("Invalid values used in the bill calculation.")
    except OverflowError:
        print("The bill is too large to calculate.")
    return None


def add_room():
    room_number = input("Enter room number: ").strip()
    if room_number == "":
        print("Room number cannot be empty.")
        return

    if find_room(room_number) is not None:
        print("This room number already exists.")
        return

    print("1. Standard  2. Deluxe  3. Suite")
    try:
        type_number = int(input("Select room type number: "))
        if type_number < 1:
            print("Room type number must be 1 or higher.")
            return
        room_type = ROOM_TYPES[type_number - 1]
    except ValueError:
        print("Invalid input. Enter the number of the room type.")
        return
    except IndexError:
        print("That room type number is not on the list.")
        return

    try:
        nightly_rate = float(input("Enter nightly rate: "))
    except ValueError:
        print("Invalid nightly rate. Enter a valid number.")
        return

    # written this way so that "nan" is rejected too
    if not (0 < nightly_rate < 100000):
        print("Nightly rate must be between 0 and 100000.")
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

    if calculate_bill(room["nightly_rate"], nights, 0) is None:
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
        charge = calculate_bill(booking["nightly_rate"],
                                booking["number_of_nights"], 0)

        print("Room Number:", room_number)
        print("Customer Name:", booking["customer_name"])
        print("Room Type:", booking["room_type"])
        print("Nightly Rate: $" + format(booking["nightly_rate"], ".2f"))
        print("Number of Nights:", booking["number_of_nights"])
        print("Estimated Room Charge: $" + format(charge, ".2f"))
        print("------------------------------------")


def get_discount():
    """Ask for a discount percentage. Return None if it is not valid."""
    text = input("Enter discount percentage (press Enter for none): ").strip()
    if text == "":
        return 0

    try:
        discount = ast.literal_eval(text)
        if discount < 0 or discount > 100:
            print("Discount must be between 0 and 100.")
            return None
        return discount
    except SyntaxError:
        print("The discount was not typed correctly.")
    except ValueError:
        print("The discount must be a number.")
    except TypeError:
        print("The discount must be a number.")
    return None


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

    discount = get_discount()
    if discount is None:
        return

    booking = allocations_dict[room_number]
    nights = booking["number_of_nights"]
    total_bill = calculate_bill(booking["nightly_rate"], nights, discount)
    if total_bill is None:
        return

    try:
        average_per_night = total_bill / nights
    except ZeroDivisionError:
        average_per_night = 0

    print("\n===== GUEST BILL =====")
    print("Room Number:", room_number)
    print("Customer Name:", booking["customer_name"])
    print("Nightly Rate: $" + format(booking["nightly_rate"], ".2f"))
    print("Number of Nights:", nights)
    print("Discount:", str(discount) + "%")
    print("Average Cost Per Night: $" + format(average_per_night, ".2f"))
    print("Total Bill: $" + format(total_bill, ".2f"))

    save_bill_to_file(room_number, booking["customer_name"], total_bill)

    del allocations_dict[room_number]
    room["available"] = True

    print("Checkout completed successfully.")
    print("Room", room_number, "is now available.")


def save_bill_to_file(room_number, customer_name, total_bill):
    """Add the checkout bill to the data file."""
    try:
        file = open(DATA_FILE, "a")
        file.write("Bill - Room: " + room_number + ", ")
        file.write("Customer: " + customer_name + ", ")
        file.write("Total: $" + format(total_bill, ".2f") + "\n\n")
        file.close()
    except IOError:
        print("The bill could not be saved to the file.")


def save_allocations_to_file():
    """Save the current allocations to the data file."""
    if len(allocations_dict) == 0:
        print("There are no allocations to save.")
        return

    try:
        file = open(DATA_FILE, "a")
        file.write("Saved on: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n")
        for room_number in allocations_dict:
            booking = allocations_dict[room_number]
            file.write("Room: " + room_number + ", ")
            file.write("Customer: " + booking["customer_name"] + ", ")
            file.write("Type: " + booking["room_type"] + ", ")
            file.write("Rate: " + str(booking["nightly_rate"]) + ", ")
            file.write("Nights: " + str(booking["number_of_nights"]) + "\n")
        file.write("\n")
        file.close()
        print("Allocations saved to", DATA_FILE)
    except IOError:
        print("The file could not be written.")


def show_allocations_from_file():
    """Read the data file and show its content."""
    try:
        file = open(DATA_FILE, "r")
        content = file.read()
        file.close()
    except FileNotFoundError:
        print("File", DATA_FILE, "was not found. Save allocations first.")
        return
    except IOError:
        print("The file could not be opened.")
        return

    if content.strip() == "":
        print("The file is empty.")
        return

    print("\n===== ALLOCATIONS FROM FILE =====")
    print(content)


def backup_and_clear_file():
    """Copy the data file into a backup file, then empty the data file."""
    time_stamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    backup_name = "LHMS_" + STUDENT_ID + "_Backup_" + time_stamp + ".txt"

    try:
        file = open(DATA_FILE, "r")
        content = file.read()
        file.close()

        if content.strip() == "":
            print("The file is empty. Nothing to back up.")
            return

        backup = open(backup_name, "a")
        backup.write(content)
        backup.close()

        file = open(DATA_FILE, "w")
        file.close()

        print("Backup saved as", backup_name)
        print(DATA_FILE, "has been cleared.")
    except FileNotFoundError:
        print("File", DATA_FILE, "was not found. Nothing to back up.")
    except IOError:
        print("The backup could not be completed.")


if __name__ == "__main__":
    main()