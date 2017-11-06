from paymentwall.httpaction import Httpaction
from paymentwall.base import Paymentwall
import json

class ApiObject(Paymentwall, Httpaction):
    API_BRICK_SUBPATH = 'brick'
    API_OBJECT_CHARGE = 'charge'
    API_OBJECT_SUBSCRIPTION = 'subscription'
    API_OBJECT_ONE_TIME_TOKEN = 'token'
    BRICK_ENDPOINTS = (API_OBJECT_CHARGE, API_OBJECT_SUBSCRIPTION, API_OBJECT_ONE_TIME_TOKEN)

    api_response = {}

    def __init__(self, id='', obj=''):
        self.id = id
        self.obj = obj

    def get_endpoint_name(self):
        if self.obj and self.obj in self.BRICK_ENDPOINTS:
            return self.obj
        else:
            return ''

    def get_api_url(self):
        if self.obj == 'token' and self.is_test() == False:
            return 'https://pwgateway.com/api/token'
        else:
            return self.BASE + '/' + self.API_BRICK_SUBPATH + '/' + self.get_endpoint_name()

    def get_api_header(self):
        return {'X-ApiKey': self.get_secret_key()} if self.obj != 'token' else {}

    def build_query(self, params):
        query = ''
        for key, value in params.items():
            query = query + '&' + key + '=' + value
        return query

    def do_api_action(self, action='', params={}, method='post'):
        action_url = self.get_api_url() + '/' + self.id + '/' + action
        http_action = Httpaction(action_url, params=params, header=self.get_api_header()) if method == 'post' else Httpaction(action_url + self.build_query(params), params={}, header={})
        response = http_action.api_request(method=method).text
        self.set_response(json.loads(response))

    def set_response(self, response):
        if response:
            self.api_response = response
            return
        else:
            return 'Empty response'

    def get_response(self):
        return self.api_response

    def get_public_data(self):
        response = self.get_response()
        result = {}
        if 'type' in response and response['type'] == 'Error':
            result = {
                'success': 0,
                'error': {
                    'message': response['error'],
                    'code': response['code']
                }
            }
        elif 'secure' in response and not self.object_response():
            result = {
                'success': 0,
                'secure': response['secure']
            }
        elif self.object_response():
            result['success'] = 1
        else:
            result = {
                'success': 0,
                'error': {
                    'message': 'Internal error'
                }
            }
        return result

    def create(self, params):
        http_action = Httpaction(self.get_api_url(), params, self.get_api_header())
        response = http_action.api_request().text
        self.set_response(json.loads(response))

    def object_response(self):
        return True if self.get_response()['object'] else False