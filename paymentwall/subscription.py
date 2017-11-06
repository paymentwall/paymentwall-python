from paymentwall.apiobject import ApiObject

class Subscription(ApiObject):
    def __init__(self, id=''):
        ApiObject.__init__(self, id=id, obj='subscription') if id else ApiObject.__init__(self, obj='subscription')

    def get_id(self):
        return self.id

    def get(self):
        return self.do_api_action()

    def is_test(self):
        return self.get_response()['test']

    def is_trial(self):
        return self.get_response()['is_trial']

    def is_active(self):
        return self.get_response()['active']

    def is_expired(self):
        return self.get_response()['expired']

    def is_successful(self):
        return self.object_response()

    def cancel(self):
        return self.do_api_action('cancel')