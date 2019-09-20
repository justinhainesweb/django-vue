import json
import requests
from project.settings import EMAIL_VERIFIER_API_KEY


class EmailVerifier:

    @staticmethod
    def lookup(email: str) -> dict:
        """
        Success response >>
        'email' = {str} 'oleksii.v.velychko@gmail.com'
        'smtp_code' = {int} 250
        'smtp_log' = {str} 'Success'
        'status' = {int} 1
        'status_description' = {str} 'OK email'

        Failure response >>
        'email' = {str} 'testov@testov.dev'
        'smtp_code' = {int} -1
        'smtp_log' = {str} 'Domain does not exist.\r MX record about this domain does not exist.\r'
        'status' = {int} 0
        'status_description' = {str} 'invalid domain'

        :param email:
        :return:
        """
        if not EMAIL_VERIFIER_API_KEY:
            return {
                'status': 0,
                'status_description': 'EMAIL_VERIFIER_API_KEY is empty'
            }

        url = f'https://app.verify-email.org/api/v1/{EMAIL_VERIFIER_API_KEY}/verify/{email}'

        try:
            r = requests.get(url)
            return json.loads(r.text)
        except (TypeError, IndexError, KeyError, requests.exceptions.HTTPError):
            return {
                'status': 0,
                'status_description': 'invalid domain'
            }
