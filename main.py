
# File: LHMS_850010874.py
# Author: Anmoldeep Singh
# Description: Langham Hotel Management System
# Date: 22 October 2026

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
                print("Add Room selected.")
            elif choice == "2":
                print("Delete Room selected.")
            elif choice == "3":
                print("Display Room Details selected.")
            elif choice == "4":
                print("Allocate Room selected.")
            elif choice == "5":
                print("Display Allocation Details selected.")
            elif choice == "6":
                print("Billing and De-Allocation selected.")
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


if __name__ == "__main__":
    main()
