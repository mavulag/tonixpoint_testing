import requests
from django.conf import settings
from django.core.exceptions import ValidationError

class AzamPayService:
    SANDBOX_AUTH_BASE_URL = 'https://authenticator-sandbox.azampay.co.tz'
    SANDBOX_BASE_URL = 'https://sandbox.azampay.co.tz'
    BASE_URL = 'https://checkout.azampay.co.tz'
    AUTH_BASE_URL = 'https://authenticator.azampay.co.tz'
    SUPPORTED_MNO = ['Airtel', 'Tigo', 'Halopesa', 'Azampesa']
    SUPPORTED_BANK = ['CRDB', 'NMB']
    SUPPORTED_CURRENCY = ['TZS']


    def __init__(self):
        if not settings.AZAMPAY_APP_NAME:
            raise ValidationError('Missing required option: AZAMPAY_APP_NAME')
        if not settings.AZAMPAY_CLIENT_ID:
            raise ValidationError('Missing required option: AZAMPAY_CLIENT_ID')
        if not settings.AZAMPAY_CLIENT_SECRET:
            raise ValidationError('Missing required option: AZAMPAY_CLIENT_SECRET')

        if settings.AZAMPAY_ENVIRONMENT == 'sandbox':
            self.base_url = self.SANDBOX_BASE_URL
            self.auth_base_url = self.SANDBOX_AUTH_BASE_URL
        else:
            self.base_url = self.BASE_URL
            self.auth_base_url = self.AUTH_BASE_URL

        self.token = self.generate_token()

    def generate_token(self):
        print(settings.AZAMPAY_APP_NAME, settings.AZAMPAY_CLIENT_ID, settings.AZAMPAY_CLIENT_SECRET)
        
        response = requests.post(
            f'{self.auth_base_url}/AppRegistration/GenerateToken',
            json={
                'appName': settings.AZAMPAY_APP_NAME,
                'clientId': settings.AZAMPAY_CLIENT_ID,
                'clientSecret': settings.AZAMPAY_CLIENT_SECRET,
            }
        )
        
        if response.status_code == 200:
            return response.json()['data']['accessToken']
        elif response.status_code == 423:
            raise ValidationError('Provided detail is not valid for this app or secret key has been expired')
        elif response.status_code >= 500:
            raise ValidationError('There is a problem with the payment processing server.')
        else:
            raise Exception('An unexpected error occurred.')

    def mobile_checkout(self, data):
        response = self.send_request('POST', '/azampay/mno/checkout', data)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise Exception(response.text)
        elif response.status_code >= 500:
            raise Exception('There is a problem with the payment processing server.')
        else:
            raise Exception('An unexpected error occurred.')

    def send_request(self, method, uri, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        url = f'{self.base_url}{uri}'
        return requests.request(method, url, json=data, headers=headers)
