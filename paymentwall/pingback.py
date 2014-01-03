from paymentwall.base import Paymentwall
from paymentwall.product import Product

import collections


class Pingback(Paymentwall):

	PINGBACK_TYPE_REGULAR = 0
	PINGBACK_TYPE_GOODWILL = 1
	PINGBACK_TYPE_NEGATIVE = 2

	def __init__(self, parameters = {}, ip_address=''):
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
		signature_params_to_sign = collections.OrderedDict()

		if self.get_api_type() == self.API_VC:
			signature_params = ['uid', 'currency', 'type', 'ref']
		elif self.get_api_type() == self.API_GOODS:
			signature_params = ['uid', 'goodsid', 'slength', 'speriod', 'type', 'ref']
		else:
			signature_params = ['uid', 'goodsid', 'type', 'ref']
			self.parameters['sign_version'] = self.SIGNATURE_VERSION_2

		if not 'sign_version' in self.parameters or int(self.parameters['sign_version']) == self.SIGNATURE_VERSION_1:
			for field in signature_params:
				signature_params_to_sign[field] = self.parameters[field] if field in self.parameters else None
			self.parameters['sign_version'] = self.SIGNATURE_VERSION_1
		else:
			signature_params_to_sign = self.parameters

		signature_calculated = self.calculate_signature(
			signature_params_to_sign, self.get_secret_key(), self.parameters['sign_version'])

		signature = self.parameters['sig'] if 'sig' in self.parameters else None

		return signature == signature_calculated

	def is_ip_address_valid(self):
		ips_whitelist = [
			'174.36.92.186',
			'174.36.96.66',
			'174.36.92.187',
			'174.36.92.192',
			'174.37.14.28'
		]

		return self.ip_address in ips_whitelist

	def is_parameters_valid(self):
		errors_number = 0

		if self.get_api_type() == self.API_VC:
			required_params = ['uid', 'currency', 'type', 'ref', 'sig']
		else:
			required_params = ['uid', 'goodsid', 'type', 'ref', 'sig']

		for field in required_params:
			if not field in self.parameters:
				self.append_to_errors('Parameter ' + field + ' is missing')
				errors_number += 1

		return errors_number == 0

	def get_parameter(self, param):
		return self.parameters[param] if param in self.parameters else None

	def get_type(self):
		if 'type' in self.parameters:
			if self.parameters['type'] in [self.PINGBACK_TYPE_REGULAR, self.PINGBACK_TYPE_GOODWILL, self.PINGBACK_TYPE_NEGATIVE]:
				return self.parameters['type']

	def get_user_id(self):
		return self.get_parameter('uid')

	def get_vc_amount(self):
		return self.get_parameter('currency')

	def get_product_id(self):
		return self.get_parameter('goodsid')

	def get_product_period_length(self):
		return self.get_parameter('slength')

	def get_product_period_type(self):
		return self.get_parameter('speriod')

	def get_product(self):
		return Product(
			self.get_product_id(),
			0,
			None,
			None,
			Product.TYPE_SUBSCRIPTION if int(self.get_product_period_length()) > 0 else Product.TYPE_FIXED,
			int(self.get_product_period_length()),
			self.get_product_period_type()
		)

	def get_products(self):
		result = []
		product_ids = self.get_parameter('goodsid')

		if type(product_ids).__name__ == 'list' and len(product_ids) > 0:
			for product_id in range(len(product_ids)):
				result.append(Product(product_ids[product_id]))

		return result

	def get_reference_id(self):
		return self.get_parameter('ref')

	def get_pingback_unique_id(self):
		return self.get_reference_id() + '_' + self.get_type()

	def is_deliverable(self):
		return self.get_type() == self.PINGBACK_TYPE_REGULAR or self.get_type() == self.PINGBACK_TYPE_GOODWILL

	def is_cancelable(self):
		return self.get_type() == self.PINGBACK_TYPE_NEGATIVE

	def calculate_signature(self, params, secret, version):
		base_string = ''
		is_array = lambda var: isinstance(var, (list, tuple))

		params = params.copy()

		if 'sig' in params:
			del params['sig']

		sortable = (int(version) == self.SIGNATURE_VERSION_2)
		keys = list(sorted(params.keys())) if sortable else list(params.keys())

		for k in range(len(keys)):
			if is_array(params[keys[k]]):
				for i in range(len(params[keys[k]])):
					base_string += str(keys[k]) + '[' + str(i) + ']=' + str(params[keys[k]][i])
			else:
				base_string += str(keys[k]) + '=' + str(params[keys[k]])

		base_string += secret

		return self.hash(base_string, 'sha256') if int(version) == self.SIGNATURE_VERSION_3 else self.hash(base_string, 'md5')