from paymentwall.apiobject import ApiObject

class Charge(ApiObject):
    def __init__(self, id=''):
        ApiObject.__init__(self, id=id, obj='charge') if id else ApiObject.__init__(self, obj='charge')

    def get_id(self):
        return self.id

    def get_token(self):
        return self.get_response()['card']['token']

    def is_test(self):
        return self.get_response()['test']

    def is_captured(self):
        return self.get_response()['captured']

    def is_successful(self):
        return self.object_response()

    def is_under_review(self):
        return self.get_response()['risk'] == 'pending'

    def is_refunded(self):
        return self.get_response()['refunded']

    def refund(self):
        return self.do_api_action(action='refund')

    def capture(self):
        return self.do_api_action(action='capture')

    def void(self):
        return self.do_api_action(action='void')