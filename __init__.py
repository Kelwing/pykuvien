import magic
import requests
import os

from .image import Image
from .domain import Domain
from .error import MissingAuthError, HttpError


class Api():
    def __init__(self, key=None, id_token=None, access_token=None):
        self.key = key
        self.id_token = id_token
        self.access_token = access_token
        self.apibase = 'https://api.kuvien.io'

    def get_auth_header(self):
        return {
            'Authorization': "Bearer {}".format(self.id_token),
            'AccessToken': self.access_token
        }

    def auth(func):
        def wrapper(self):
            if not self.id_token and not self.access_token:
                raise MussingAuthError
            else:
                return func(self)
        return wrapper

    def upload(self, f):
        if not self.key:
            raise MissingAuthError

        mime = magic.Magic(mime=True)
        if isinstance(f, str):
            is_fo = False
        else:
            is_fo = True

        fo = f if is_fo else open(f, 'rb')
        filename = os.path.basename(f.name) if is_fo else f
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

        if not resp.status_code == 200:
            raise HttpError(resp.json()['status'], resp.status_code)

        re = resp.json()['file']
        image = Image(re['url'], f.name, self.id_token, self.access_token)
        return image

    def domains(self):
        resp = requests.get('{}/domains'.format(self.apibase))
        print(resp.status_code)
        if not resp.status_code == 200:
            raise HttpError(resp.json()['status'], resp.status_code)

        return resp.json()['domains']

    @auth
    def list_subdomains(self):

        resp = requests.get(
            '{}/user/domains'.format(self.apibase),
            headers=self.get_auth_header()
        )

        if not resp.status_code == 200:
            print(resp.status_code)
            raise HttpError(resp.json()['status'], resp.status_code)

        domains = resp.json()['domains']
        ds = list()
        for domain in domains:
            d = Domain(
                    domain['domain'],
                    domain['subdomain'],
                    domain['key'],
                    self.id_token,
                    self.access_token)
            ds.append(d)
        return ds

    @auth
    def add_subdomain(self, subdomain, domain):
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
            raise HttpError(resp.json()['status'], resp.status_code)

        d = resp.json()
        domain = Domain(
                d['subdomain'],
                d['domain'],
                d['key'],
                self.id_token,
                self.access_token)
        return domain

    @auth
    def list_images(self, page=0):
        if page == 0:
            endpoint = '/user/images'
        else:
            endpoint = '/user/images/{}'.format(page)

        resp = requests.get(
            '{}{}'.format(self.apibase, endpoint),
            headers=self.get_auth_header()
        )

        if not resp.status_code == 200:
            raise HttpError(resp.json()['status'], resp.status_code)

        images = list()
        for i in resp.json()['images']:
            url = "https://" + i['subdomain'] + '.' + i['domain'] + "/" + i['_id']
            u = Image(url, i['originalname'], self.id_token, self.access_token, i['mature'])
            images.append(u)

        return images

    @auth
    def get(self, id):
        resp = request.get(
                '{}/user/image/{}'.format(self.apibase, id),
                headers=self.get_auth_header()
                )

        if not resp.status_code == 200:
            raise HttpError(resp.json()['status'], resp.status_code)

        raw_img = resp.json()['image']
        return Image(
                "https://" + raw_img['subdomain'] + '.' + raw_img['domain'] + '/' + raw_img['_id'],
                raw_img['originalname'],
                self.id_token,
                self.access_token,
                raw_img['mature'])


if __name__ == '__main__':
    pass
