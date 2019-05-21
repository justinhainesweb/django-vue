import json
import requests
from project.settings import EMAIL_VERIFIER_API_KEY


class EmailVerifier:

    @staticmethod
    def lookup(email: str) -> str:
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

        url = f'https://app.verify-email.org/api/v1/{EMAIL_VERIFIER_API_KEY}/verify/{email}'

        try:
            r = requests.get(url)
            parsed = json.loads(r.text)
            if parsed.get('status', 0) == 0:
                return parsed.get('status_description', 'invalid domain')
        except (TypeError, IndexError, KeyError, requests.exceptions.HTTPError):
            return 'invalid domain'

        return parsed.get('status_description', 'valid domain')
