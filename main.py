from logon import logon as l


if __name__ == "__main__":
    print("Welcome to Freedom Mobile MyAccount!")
    print("Please enter your phone number and pin.")

    phone_number = input("Phone number: ")
    pin = input("Pin: ")

    response = l.logon(phone_number, pin)

    if not response:
        print("Logon failed!")
        exit()

    tmp_hash = response["tmpHash"]
    l.send_verification(response)
    response, cookies = l.validate_security_code(tmp_hash)

    if response["Result"] != "AuthUserSuccess":
        print("Verification failed!")
        exit()

    encrypted_token = l.get_dsl_token(cookies)
    service_item = l.service_item(cookies)
    l.authenticate(encrypted_token)

    print("Done")



