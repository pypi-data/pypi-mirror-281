import requests
from .auth import _token
from .auth import _credentials
from .auth import _request_headers
from .utils import _get_private_ip
from .utils import _get_fqdn_id
from .utils import _create_ca
from .utils import _create_cert
from .utils import _get_ca
from .utils import _get_certs

class CA(object):
    access_key = None
    secret_key = None
    email = None
    public_ip = None
    private_ip = None
    token = None
    request_headers = None
    def __init__(self):
        self.access_key, self.secret_key, self.email = _credentials()
        self.public_ip = requests.get('https://devnull.cn/ip').json()['origin']
        self.private_ip = _get_private_ip()
        self.token = _token(self.email, self.access_key, self.secret_key)
        self.request_headers = _request_headers(token=self.token)
        self.fqdn = _get_fqdn_id() + '.public.thedns.cn'
    def get_ca(self):
        return _get_ca(request_headers=self.request_headers)
    def get_certs(self):
        return _get_certs(request_headers=self.request_headers)
    def create_ca(self):
        return _create_ca(request_headers=self.request_headers)
    def create_cert(self):
        return _create_cert(request_headers=self.request_headers,common_name=self.fqdn)

"""
import theca; ca = theca.CA(); ca.get_ca()


"""