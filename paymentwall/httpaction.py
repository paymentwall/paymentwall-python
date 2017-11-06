import requests

class Httpaction():
    def __init__(self, baseurl, params, header):
        self.baseurl = baseurl
        self.params = params
        self.header = header

    def get_base_url(self):
        return self.baseurl

    def get_request_params(self):
        return self.params

    def get_header_params(self):
        return self.header

    def api_request(self, method='post'):
        request_object = requests.post(self.baseurl, data=self.params, headers=self.header)
        if method == 'get':
            request_object = requests.get(self.baseurl, data=self.params, headers=self.header)
        return request_object