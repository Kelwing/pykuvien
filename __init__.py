import magic
import requests
import os


class MissingAuthError(Exception):
    pass


class HttpError(Exception):
    pass


class Api():
    def __init__(self, key=None, id_token=None, access_token=None):
        self.key = key
        self.id_token = id_token
        self.access_token = access_token
        self.apibase = 'https://api.kuvien.io'

    def get_auth_header(self):
        return {
            'Authorization': self.id_token,
            'AccessToken': self.access_token
        }

    def upload(self, f):
        if not self.key:
            raise MissingAuthError

        mime = magic.Magic(mime=True)
        if isinstance(f, str):
            is_fo = False
        else:
            is_fo = True

        filename = os.path.basename(f.name) if is_fo else f
        fo = f if is_fo else open(f, 'rb')
        mimetype = mime.from_buffer(fo.read(1024))

        form_data = {
            'file': (filename, fo, mimetype)
        }

        headers = {
            'x-app-key': self.key
        }

        resp = requests.post(
            '{}/image/upload'.format(self.apibase),
            files=form_data,
            headers=headers
        )

        return resp.json()['file']['url']

    def domains(self):
        resp = requests.get('{}/domains'.format(self.apibase))

        if not resp.status_code == 200:
            raise HttpError

        return resp.json()['domains']

    def list_subdomains(self):
        if not self.id_token or not self.access_token:
            raise MissingAuthError

        resp = requests.get(
            '{}/user/domains'.format(self.apibase),
            headers=self.get_auth_header()
        )

        if not resp.status_code == 200:
            raise HttpError

        return resp.json()['domains']

    def add_subdomain(self, subdomain, domain):
        if not self.id_token or not self.access_token:
            raise MissingAuthError

        payload = {
            'domain': domain,
            'subdomain': subdomain
        }

        resp = requests.post(
            '{}/domain/add'.format(self.apibase),
            json=payload,
            headers=self.get_auth_header()
        )

        if not resp.status_code == 200:
            raise HttpError

        return resp.json()

    def remove_subdomain(self, domainkey):
        if not self.id_token or not self.access_token:
            raise MissingAuthError

        payload = {
            'key': domainkey
        }

        resp = requests.post(
            '{}/user/domain/delete'.format(self.apibase),
            json=payload,
            headers=self.get_auth_header()
        )

        if not resp.status_code == 200:
            raise HttpError

        return resp.json()


if __name__ == '__main__':
    pass
