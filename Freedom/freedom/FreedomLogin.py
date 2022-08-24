import requests


class FreedomLogin:
    """
    A class containing methods to log in to a Freedom Mobile account.
    """

    def __init__(self, phone_number: str, pin: str):
        """
        Initialize the FreedomLogin class.
        """
        self.phone_number = phone_number
        self.pin = pin

        self._token = None
        self._encrypted_token = None
        self._cookies = None
        self._service_item = None

    def login(self) -> bool:
        """
        Log on to the Freedom Mobile MyAccount website.
        :return:
        """
        url = "https://carerest.freedommobile.ca/selfcare/v1/users/token"
        data = {
            "msisdn": self.phone_number,
            "pin": self.pin,
            "FacebookToken": ""
        }
        r = requests.post(url, json=data)

        if r.status_code != 411:
            return False

        self._token = r.json()["tmpHash"]
        self._send_verification_code(r.json())
        response, self._cookies = self._validate_security_code()

        if response["Result"] != "AuthUserSuccess":
            return False

        self._get_encrypted_token()
        self._get_service_item()

        return True

    def _send_verification_code(self, r: dict) -> None:
        """
        Send the verification code to the user-specified medium.
        :param r:
        :return:
        """
        communication_channels = r["CommunicationChannels"]
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
        self._send_verification_request(list(channels[channel_number]))

    def _send_verification_request(self, channel: list) -> None:
        """
        Send a verification request to the selected channel.
        :param channel:
        :param token:
        :return:
        """
        url = "https://carerest.freedommobile.ca/selfcare/v1/users/sendSecurityCode"
        data = {
            "tmpTkn": self._token,
            "userInput": channel[2],
            "userInputType": channel[1]
        }
        r = requests.post(url, json=data)

        if r.status_code != 200:
            exit()

    def _validate_security_code(self) -> tuple:
        """
        Validate the security code.
        :return:
        """
        url = "https://carerest.freedommobile.ca/selfcare/v1/users/validateSecurityCode"
        data = {
            "tmpTkn": self._token,
            "userInput": input("Enter the security code: "),
            "trustThisComputer": False,
            "platform": "web"
        }
        r = requests.post(url, json=data)

        if r.status_code != 200:
            exit()

        return r.json(), r.cookies

    def _get_encrypted_token(self) -> None:
        """
        Get the encrypted token.
        :return:
        """
        url = "https://carerest.freedommobile.ca/selfcare/v1/users/dslToken"
        r = requests.get(url, cookies=self._cookies)

        if r.status_code != 200:
            exit()

        self._encrypted_token = r.json()["encryptedToken"]

    def _get_service_item(self) -> None:
        """
        Get the service item.
        :return:
        """
        url = "https://carerest.freedommobile.ca/selfcare/v1/serviceitem"
        r = requests.get(url, cookies=self._cookies)

        self._service_item = r.json()

    def authenticate(self) -> bool:
        """
        Authenticate the user.
        :return:
        """
        url = "https://api.freedommobile.ca/api/v1/authentication/authenticate"
        data = {
            "token": self._encrypted_token
        }
        r = requests.post(url, json=data)

        if r.status_code != 204:
            return False

        return True

    def get_service_item(self) -> dict:
        """
        Get the service item.
        :return:
        """
        return self._service_item
