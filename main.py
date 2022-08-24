from freedom.FreedomLogin import FreedomLogin
from freedom.FreedomAccount import account_from_service_item
import json

# TODO: Print general info

if __name__ == "__main__":
    print("Welcome to Freedom Mobile MyAccount!")
    print("Please enter your phone number and pin.")

    phone_number = input("Phone number: ")
    pin = input("Pin: ")

    fl = FreedomLogin(phone_number, pin)
    fl.login()
    fl.authenticate()
    service_item = fl.get_service_item()

    account = account_from_service_item(service_item)

    print(json.dumps(service_item, indent=4))
