from paymentwall.base import Paymentwall
from paymentwall.product import Product

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class Pingback(Paymentwall):

    PINGBACK_TYPE_REGULAR = 0
    PINGBACK_TYPE_GOODWILL = 1
    PINGBACK_TYPE_NEGATIVE = 2

    PINGBACK_TYPE_RISK_UNDER_REVIEW = 200
    PINGBACK_TYPE_RISK_REVIEWED_ACCEPTED = 201
    PINGBACK_TYPE_RISK_REVIEWED_DECLINED = 202

    PINGBACK_TYPE_RISK_AUTHORIZATION_VOIDED = 203

    PINGBACK_TYPE_SUBSCRIPTION_CANCELLATION = 12
    PINGBACK_TYPE_SUBSCRIPTION_EXPIRED = 13
    PINGBACK_TYPE_SUBSCRIPTION_PAYMENT_FAILED = 14

    def __init__(self, parameters={}, ip_address=''):
        self.parameters = parameters
        self.ip_address = ip_address

    def validate(self, skip_ip_whitelist_check=False):
        validated = False

        if self.is_parameters_valid():
            if self.is_ip_address_valid() or skip_ip_whitelist_check:
                if self.is_signature_valid():
                    validated = True
                else:
                    self.append_to_errors('Wrong signature')
            else:
                self.append_to_errors('IP address is not whitelisted')
        else:
            self.append_to_errors('Missing parameters')

        return validated

    def is_signature_valid(self):
        signature_params_to_sign = OrderedDict()

        if self.get_api_type() == self.API_VC:
            signature_params = ['uid', 'currency', 'type', 'ref']
        elif self.get_api_type() == self.API_GOODS:
            signature_params = ['uid', 'goodsid', 'slength', 'speriod', 'type', 'ref']
        else:
            signature_params = ['uid', 'goodsid', 'type', 'ref']
            self.parameters['sign_version'] = self.SIGNATURE_VERSION_2

        if 'sign_version' not in self.parameters or int(self.parameters['sign_version']) == self.SIGNATURE_VERSION_1:
            for field in signature_params:
                signature_params_to_sign[field] = self.parameters[field] if field in self.parameters else None
            self.parameters['sign_version'] = self.SIGNATURE_VERSION_1
        else:
            signature_params_to_sign = self.parameters

        signature_calculated = self.calculate_signature(
            signature_params_to_sign, self.get_secret_key(), self.parameters['sign_version']
        )

        signature = self.parameters['sig'] if 'sig' in self.parameters else None

        return signature == signature_calculated

    def is_ip_address_valid(self):
        ips_whitelist = [
            '174.36.92.186',
            '174.36.96.66',
            '174.36.92.187',
            '174.36.92.192',
            '174.37.14.28',
            '216.127.71.0',
            '216.127.71.1',
            '216.127.71.2',
            '216.127.71.3',
            '216.127.71.4',
            '216.127.71.5',
            '216.127.71.6',
            '216.127.71.7',
            '216.127.71.8',
            '216.127.71.9',
            '216.127.71.10',
            '216.127.71.11',
            '216.127.71.12',
            '216.127.71.13',
            '216.127.71.14',
            '216.127.71.15',
            '216.127.71.16',
            '216.127.71.17',
            '216.127.71.18',
            '216.127.71.19',
            '216.127.71.20',
            '216.127.71.21',
            '216.127.71.22',
            '216.127.71.23',
            '216.127.71.24',
            '216.127.71.25',
            '216.127.71.26',
            '216.127.71.27',
            '216.127.71.28',
            '216.127.71.29',
            '216.127.71.30',
            '216.127.71.31',
            '216.127.71.32',
            '216.127.71.33',
            '216.127.71.34',
            '216.127.71.35',
            '216.127.71.36',
            '216.127.71.37',
            '216.127.71.38',
            '216.127.71.39',
            '216.127.71.40',
            '216.127.71.41',
            '216.127.71.42',
            '216.127.71.43',
            '216.127.71.44',
            '216.127.71.45',
            '216.127.71.46',
            '216.127.71.47',
            '216.127.71.48',
            '216.127.71.49',
            '216.127.71.50',
            '216.127.71.51',
            '216.127.71.52',
            '216.127.71.53',
            '216.127.71.54',
            '216.127.71.55',
            '216.127.71.56',
            '216.127.71.57',
            '216.127.71.58',
            '216.127.71.59',
            '216.127.71.60',
            '216.127.71.61',
            '216.127.71.62',
            '216.127.71.63',
            '216.127.71.64',
            '216.127.71.65',
            '216.127.71.66',
            '216.127.71.67',
            '216.127.71.68',
            '216.127.71.69',
            '216.127.71.70',
            '216.127.71.71',
            '216.127.71.72',
            '216.127.71.73',
            '216.127.71.74',
            '216.127.71.75',
            '216.127.71.76',
            '216.127.71.77',
            '216.127.71.78',
            '216.127.71.79',
            '216.127.71.80',
            '216.127.71.81',
            '216.127.71.82',
            '216.127.71.83',
            '216.127.71.84',
            '216.127.71.85',
            '216.127.71.86',
            '216.127.71.87',
            '216.127.71.88',
            '216.127.71.89',
            '216.127.71.90',
            '216.127.71.91',
            '216.127.71.92',
            '216.127.71.93',
            '216.127.71.94',
            '216.127.71.95',
            '216.127.71.96',
            '216.127.71.97',
            '216.127.71.98',
            '216.127.71.99',
            '216.127.71.100',
            '216.127.71.101',
            '216.127.71.102',
            '216.127.71.103',
            '216.127.71.104',
            '216.127.71.105',
            '216.127.71.106',
            '216.127.71.107',
            '216.127.71.108',
            '216.127.71.109',
            '216.127.71.110',
            '216.127.71.111',
            '216.127.71.112',
            '216.127.71.113',
            '216.127.71.114',
            '216.127.71.115',
            '216.127.71.116',
            '216.127.71.117',
            '216.127.71.118',
            '216.127.71.119',
            '216.127.71.120',
            '216.127.71.121',
            '216.127.71.122',
            '216.127.71.123',
            '216.127.71.124',
            '216.127.71.125',
            '216.127.71.126',
            '216.127.71.127',
            '216.127.71.128',
            '216.127.71.129',
            '216.127.71.130',
            '216.127.71.131',
            '216.127.71.132',
            '216.127.71.133',
            '216.127.71.134',
            '216.127.71.135',
            '216.127.71.136',
            '216.127.71.137',
            '216.127.71.138',
            '216.127.71.139',
            '216.127.71.140',
            '216.127.71.141',
            '216.127.71.142',
            '216.127.71.143',
            '216.127.71.144',
            '216.127.71.145',
            '216.127.71.146',
            '216.127.71.147',
            '216.127.71.148',
            '216.127.71.149',
            '216.127.71.150',
            '216.127.71.151',
            '216.127.71.152',
            '216.127.71.153',
            '216.127.71.154',
            '216.127.71.155',
            '216.127.71.156',
            '216.127.71.157',
            '216.127.71.158',
            '216.127.71.159',
            '216.127.71.160',
            '216.127.71.161',
            '216.127.71.162',
            '216.127.71.163',
            '216.127.71.164',
            '216.127.71.165',
            '216.127.71.166',
            '216.127.71.167',
            '216.127.71.168',
            '216.127.71.169',
            '216.127.71.170',
            '216.127.71.171',
            '216.127.71.172',
            '216.127.71.173',
            '216.127.71.174',
            '216.127.71.175',
            '216.127.71.176',
            '216.127.71.177',
            '216.127.71.178',
            '216.127.71.179',
            '216.127.71.180',
            '216.127.71.181',
            '216.127.71.182',
            '216.127.71.183',
            '216.127.71.184',
            '216.127.71.185',
            '216.127.71.186',
            '216.127.71.187',
            '216.127.71.188',
            '216.127.71.189',
            '216.127.71.190',
            '216.127.71.191',
            '216.127.71.192',
            '216.127.71.193',
            '216.127.71.194',
            '216.127.71.195',
            '216.127.71.196',
            '216.127.71.197',
            '216.127.71.198',
            '216.127.71.199',
            '216.127.71.200',
            '216.127.71.201',
            '216.127.71.202',
            '216.127.71.203',
            '216.127.71.204',
            '216.127.71.205',
            '216.127.71.206',
            '216.127.71.207',
            '216.127.71.208',
            '216.127.71.209',
            '216.127.71.210',
            '216.127.71.211',
            '216.127.71.212',
            '216.127.71.213',
            '216.127.71.214',
            '216.127.71.215',
            '216.127.71.216',
            '216.127.71.217',
            '216.127.71.218',
            '216.127.71.219',
            '216.127.71.220',
            '216.127.71.221',
            '216.127.71.222',
            '216.127.71.223',
            '216.127.71.224',
            '216.127.71.225',
            '216.127.71.226',
            '216.127.71.227',
            '216.127.71.228',
            '216.127.71.229',
            '216.127.71.230',
            '216.127.71.231',
            '216.127.71.232',
            '216.127.71.233',
            '216.127.71.234',
            '216.127.71.235',
            '216.127.71.236',
            '216.127.71.237',
            '216.127.71.238',
            '216.127.71.239',
            '216.127.71.240',
            '216.127.71.241',
            '216.127.71.242',
            '216.127.71.243',
            '216.127.71.244',
            '216.127.71.245',
            '216.127.71.246',
            '216.127.71.247',
            '216.127.71.248',
            '216.127.71.249',
            '216.127.71.250',
            '216.127.71.251',
            '216.127.71.252',
            '216.127.71.253',
            '216.127.71.254',
            '216.127.71.255'
        ]

        return self.ip_address in ips_whitelist

    def is_parameters_valid(self):
        errors_number = 0

        if self.get_api_type() == self.API_VC:
            required_params = ['uid', 'currency', 'type', 'ref', 'sig']
        else:
            required_params = ['uid', 'goodsid', 'type', 'ref', 'sig']

        for field in required_params:
            if field not in self.parameters:
                self.append_to_errors('Parameter ' + field + ' is missing')
                errors_number += 1

        return errors_number == 0

    def get_parameter(self, param):
        return self.parameters.get(param, None)

    def get_type(self):
        if 'type' in self.parameters:
            try:
                type_parameter = int(self.parameters['type'])
            except ValueError:
                return None

            return type_parameter

    def get_user_id(self):
        return self.get_parameter('uid')

    def get_vc_amount(self):
        return self.get_parameter('currency')

    def get_product_id(self):
        return self.get_parameter('goodsid')

    def get_product_period_length(self):
        try:
            return int(self.parameters['slength'])
        except ValueError:
            return 0

    def get_product_period_type(self):
        try:
            return int(self.parameters['speriod'])
        except ValueError:
            return None

    def get_product(self):
        return Product(
            self.get_product_id(),
            0,
            None,
            None,
            Product.TYPE_SUBSCRIPTION if self.get_product_period_length() > 0 else Product.TYPE_FIXED,
            self.get_product_period_length(),
            self.get_product_period_type()
        )

    def get_products(self):
        product_ids = self.get_parameter('goodsid')

        if isinstance(product_ids, list) and product_ids:
            result = [Product(product_id) for product_id in product_ids]
        else:
            result = []

        return result

    def get_reference_id(self):
        return self.get_parameter('ref')

    def get_pingback_unique_id(self):
        return self.get_reference_id() + '_' + str(self.get_type())

    def is_deliverable(self):
        return (
            self.get_type() == self.PINGBACK_TYPE_REGULAR or
            self.get_type() == self.PINGBACK_TYPE_GOODWILL or
            self.get_type() == self.PINGBACK_TYPE_RISK_REVIEWED_ACCEPTED
        )

    def is_cancelable(self):
        return (
            self.get_type() == self.PINGBACK_TYPE_NEGATIVE or
            self.get_type() == self.PINGBACK_TYPE_RISK_REVIEWED_DECLINED
        )

    def is_under_review(self):
        return self.get_type() == self.PINGBACK_TYPE_RISK_UNDER_REVIEW

    def calculate_signature(self, params, secret, version):
        base_string = ''

        params = params.copy()

        if 'sig' in params:
            del params['sig']

        sortable = int(version) in [self.SIGNATURE_VERSION_2, self.SIGNATURE_VERSION_3]
        keys = list(sorted(params.keys())) if sortable else list(params.keys())

        for k in range(len(keys)):
            if isinstance(params[keys[k]], (list, tuple)):
                for i in range(len(params[keys[k]])):
                    base_string += str(keys[k]) + '[' + str(i) + ']=' + str(params[keys[k]][i])
            else:
                base_string += str(keys[k]) + '=' + str(params[keys[k]])

        base_string += secret

        return (
            self.hash(base_string, 'sha256')
            if int(version) == self.SIGNATURE_VERSION_3
            else self.hash(base_string, 'md5')
        )
