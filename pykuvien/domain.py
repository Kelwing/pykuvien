import requests

from .error import MissingAuthError

class Domain():
    def __init__(self, subdomain, domain, key, id_token, access_token):
        self.subdomain = subdomain
        self.domain = domain
        self.key = key
        self.id_token = id_token
        self.access_token = access_token

    def get_auth_header(self):
        return {
                'Authorization': 'Bearer {}'.format(self.id_token),
                'AccessToken': self.access_token
        }

    def __json__(self):
        return dict(
                subdomain=self.subdomain,
                domain=self.domain,
                key=self.key,
                id_token=self.id_token,
                access_token=self.access_token)

    def auth_decorator(func):
        def wrapper(self):
            if not self.id_token and not self.access_token:
                raise MissingAuthError
            else:
                return func(self)
        return wrapper

    @auth_decorator
    def delete(self):
        payload = {
                'key': self.key
                }

        resp = request.post(
                '{}/user/domain/delete'.format(self.apibase),
                json=payload,
                headers=self.get_auth_header()
                )

        if not resp.status_code == 200:
            raise HttpError(resp.json()['status'], resp.status_code)

        return resp.json()

    def regenerate_key(self):
        payload = {
                'key': self.key
                }

        resp = requests.post(
                '{}/user/domain/regenerate'.format(self.apibase),
                json=payload,
                headers=self.get_auth_header()
                )

        if not resp.status_code == 200:
            raise HttpError(resp.json()['status'], resp.status_code)

        return resp.json()
