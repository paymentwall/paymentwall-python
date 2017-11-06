from paymentwall.apiobject import ApiObject

class OneTimeToken(ApiObject):
    def __init__(self):
        ApiObject.__init__(self, obj='token')

    def get_token(self):
        return self.get_response()['token']

    def is_active(self):
        return self.get_response()['active']

    def get_expiration_time(self):
        return self.get_response()['expires_in']

