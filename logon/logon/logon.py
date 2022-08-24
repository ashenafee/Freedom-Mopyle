import requests


def logon(phone_number: str, pin: str) -> dict:
    """
    Logon to the Freedom Mobile MyAccount website and return the JSON from the response.
    :param phone_number:
    :param pin:
    :return:
    """
    url = "https://carerest.freedommobile.ca/selfcare/v1/users/token"
    data = {
        "msisdn": phone_number,
        "pin": pin,
        "FacebookToken": ""
    }
    r = requests.post(url, json=data)

    if r.status_code == 411:
        return r.json()
    else:
        return {}


def send_verification(response: dict) -> None:
    """
    Ask the user where they want to send a verification code to.
    :param response:
    :return:
    """
    communication_channels = response["CommunicationChannels"]
    channels = {}

    print("Please select a channel to send the verification code to:")
    i = 1
    for channel in communication_channels:
        if channel == "Msisdns":
            for msisdn in communication_channels[channel]:
                print(f"\t{i}. {msisdn}")
                channels[i] = (msisdn, "MSISDN")
                i += 1
        else:
            print(f"\t{i}. {channel}")
            channels[i] = (communication_channels[channel], "EMAIL")
            i += 1

    channel_number = int(input("Enter the number of the channel: "))
    channel_input = input("Enter the selected channel: ")

    channels[channel_number] = list(channels.get(channel_number))
    channels[channel_number].append(channel_input)
    _send_verification_request(list(channels[channel_number]), response["tmpHash"])


def _send_verification_request(channel: list, token: str) -> None:
    """
    Send a verification request to the selected channel.
    :param channel:
    :param token:
    :return:
    """
    url = "https://carerest.freedommobile.ca/selfcare/v1/users/sendSecurityCode"
    data = {
        "tmpTkn": token,
        "userInput": channel[2],
        "userInputType": channel[1]
    }
    r = requests.post(url, json=data)

    if r.status_code != 200:
        exit()


def validate_security_code(tmp_hash: str) -> tuple:
    """
    Validate the security code inputted by the user.
    :param tmp_hash:
    :return:
    """
    url = "https://carerest.freedommobile.ca/selfcare/v1/users/validateSecurityCode"
    data = {
        "tmpTkn": tmp_hash,
        "userInput": input("Enter the security code: "),
        "trustThisComputer": False,
        "platform": "web"
    }
    r = requests.post(url, json=data)

    if r.status_code == 200:
        return r.json(), r.cookies
    else:
        return ()


def get_dsl_token(cookies: dict) -> str:
    """
    Get the DSL token from the response.
    :param cookies:
    :return:
    """
    url = "https://carerest.freedommobile.ca/selfcare/v1/users/dslToken"
    r = requests.get(url, cookies=cookies)

    return r.json()["encryptedToken"]


def service_item(cookies: dict) -> dict:
    """
    Get the service item from the response.
    :param cookies:
    :return:
    """
    url = "https://carerest.freedommobile.ca/selfcare/v1/serviceitem"
    r = requests.get(url, cookies=cookies)

    return r.json()


def authenticate(token: str) -> None:
    """
    Authenticate the user with the DSL token.
    :param token:
    :return:
    """
    url = "https://api.freedommobile.ca/api/v1/authentication/authenticate"
    data = {
        "token": token
    }
    r = requests.post(url, json=data)

    if r.status_code == 204:
        print("Authentication successful!")
    else:
        print("Authentication failed!")
