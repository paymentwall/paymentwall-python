import hashlib


class Paymentwall:

	VERSION = '1.0.0'

	API_VC = 1
	API_GOODS = 2
	API_CART = 3
	API_CHECKOUT = 4

	VC_CONTROLLER = 'ps'
	GOODS_CONTROLLER = 'subscription'
	CART_CONTROLLER = 'cart'
	CHECKOUT_CONTROLLER = 'v1/checkout/orders'

	DEFAULT_SIGNATURE_VERSION = 3
	SIGNATURE_VERSION_1 = 1
	SIGNATURE_VERSION_2 = 2
	SIGNATURE_VERSION_3 = 3

	errors = []

	api_type = None
	app_key = None
	secret_key = None

	@classmethod
	def set_api_type(cls, api_type):
		cls.api_type = api_type

	@classmethod
	def get_api_type(cls):
		return cls.api_type

	@classmethod
	def set_app_key(cls, app_key):
		cls.app_key = app_key

	@classmethod
	def get_app_key(cls):
		return cls.app_key

	@classmethod
	def set_secret_key(cls, secret_key):
		cls.secret_key = secret_key

	@classmethod
	def get_secret_key(cls):
		return cls.secret_key

	@classmethod
	def append_to_errors(cls, err):
		cls.errors.append(err)

	@classmethod
	def get_errors(cls):
		return cls.errors

	@classmethod
	def get_error_summary(cls):
		return '\n'.join(cls.get_errors())

	#
	# Helper functions
	#
	@classmethod
	def is_empty(cls, dictionary, key):
		if isinstance(dictionary, dict):
			if key in dictionary:
				if dictionary[key]:
					return False
			return True

	@classmethod
	def array_merge(cls, first_array, second_array):
		if isinstance(first_array, list) and isinstance(second_array, list):
			return first_array + second_array
		elif isinstance(first_array, dict) and isinstance(second_array, dict):
			return dict(list(first_array.items()) + list(second_array.items()))
		elif isinstance(first_array, set) and isinstance(second_array, set):
			return first_array.union(second_array)
		return False

	@classmethod
	def hash(cls, string, library_type):
		hashed_string = hashlib.md5() if library_type == 'md5' else hashlib.sha256()
		hashed_string.update(string.encode('utf-8'))
		return hashed_string.hexdigest()

	@classmethod
	def request_calculate_signature(self, params, secret, version):
		base_string = ''
		is_array = lambda var: isinstance(var, (list, tuple))

		params = sorted(params.items())

		for i in range(len(params)):
			if is_array(params[i][1]):
				for key in range(len(params[i][1])):
					base_string += str(params[i][0]) + '[' + str(key) + ']=' + str(params[i][1][key])
			else:
				base_string += str(params[i][0]) + '=' + str(params[i][1])

		base_string += secret

		if version == self.SIGNATURE_VERSION_2:
			return self.hash(base_string, 'md5')

		return self.hash(base_string, 'sha256')