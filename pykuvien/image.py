import regex
import requests

from .error import MissingAuthError

imagex = regex.compile(r"(?:https:\/\/)(.+?)\.(.+?)\/(.+)")

class Image():
    def __init__(self, url, name, id_token, access_token, mature=False):
        self.url = url
        self.name = name
        self.id_token = id_token
        self.access_token = access_token
        match = imagex.match(self.url)
        self.subdomain = match.group(1)
        self.domain = match.group(2)
        self.id = match.group(3)
        self.apibase = 'https://api.kuvien.io'
        self.mature = mature

    def get_auth_header(self):
        return {
            'Authorization': "Bearer {}".format(self.id_token),
            'AccessToken': self.access_token
        }

    def auth_decorator(func, *args, **kwargs):
        def wrapper(self, *args, **kwargs):
            if not self.id_token or not self.access_token:
                raise MissingAuthError
            else:
                return func(self, *args, **kwargs)
        return wrapper

    @auth_decorator
    def delete(self):
        payload = {
            'id': id
        }

        resp = request.get(
            '{}/user/image/delete'.format(self.apibase),
            json=payload,
            headers=self.get_auth_header()
        )

        if not resp.status_code == 200:
            raise HttpError(resp.json()['status'], resp.status_code)

        return resp.json()['status']

    def __json__(self, req):
        return dict(
                url=self.url,
                name=self.name,
                domain=self.domain,
                subdomain=self.subdoamin,
                id_token=self.id_token,
                access_token=self.access_token,
                mature=self.mature)
