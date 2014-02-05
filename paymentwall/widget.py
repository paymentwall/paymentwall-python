from paymentwall.base import Paymentwall
from paymentwall.product import Product

import re

try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode


class Widget(Paymentwall):

	BASE_URL = 'https://api.paymentwall.com/api'

	def __init__(self, user_id, widget_code, products=[], extra_params={}):
		self.user_id = user_id
		self.widget_code = widget_code
		self.extra_params = extra_params
		self.products = products

	def get_default_widget_signature(self):
		return self.DEFAULT_SIGNATURE_VERSION if self.get_api_type() != self.API_CART else self.SIGNATURE_VERSION_2

	def get_url(self):
		params = {
			'key': self.get_app_key(),
			'uid': self.user_id,
			'widget': self.widget_code
		}

		products_number = len(self.products)

		if self.get_api_type() == self.API_GOODS:

			if isinstance(self.products, list):

				if products_number == 1:
					product = self.products[0]

					if isinstance(product, Product):
						post_trial_product = None

						if isinstance(product.get_trial_product(), Product):
							post_trial_product = product
							product = product.get_trial_product()

						params['amount'] = product.get_amount()
						params['currencyCode'] = product.get_currency_code()
						params['ag_name'] = product.get_name()
						params['ag_external_id'] = product.get_id()
						params['ag_type'] = product.get_type()

						if product.get_type() == Product.TYPE_SUBSCRIPTION:
							params['ag_period_length'] = product.get_period_length()
							params['ag_period_type'] = product.get_period_type()

							if product.is_recurring():
								params['ag_recurring'] = 1 if product.is_recurring() else 0

								if post_trial_product:
									params['ag_trial'] = 1
									params['ag_post_trial_external_id'] = post_trial_product.get_id()
									params['ag_post_trial_period_length'] = post_trial_product.get_period_length()
									params['ag_post_trial_period_type'] = post_trial_product.get_period_type()
									params['ag_post_trial_name'] = post_trial_product.get_name()
									params['post_trial_amount'] = post_trial_product.get_amount()
									params['post_trial_currencyCode'] = post_trial_product.get_currency_code()
					else:
						self.append_to_errors('Not a Product instance')
				else:
					self.append_to_errors('Only 1 product is allowed')

		elif self.get_api_type() == self.API_CART:
			index = 0

			for product in self.products:
				params['external_ids[' + str(index) + ']'] = product.get_id()
				if product.get_amount() > 0:
					params['prices[' + str(index) + ']'] = product.get_amount()
				if product.get_currency_code() != '' and product.get_currency_code() is not None:
					params['currencies[' + str(index) + ']'] = product.get_currency_code()
				index += 1

		params['sign_version'] = signature_version = str(self.get_default_widget_signature())

		if not self.is_empty(self.extra_params, 'sign_version'):
			signature_version = params['sign_version'] = str(self.extra_params['sign_version'])

		params = self.array_merge(params, self.extra_params)

		params['sign'] = self.calculate_signature(params, self.get_secret_key(), int(signature_version))

		return self.BASE_URL + '/' + self.build_controller(self.widget_code) + '?' + urlencode(params)

	def get_html_code(self, attributes={}):
		default_attributes = {
			'frameborder': '0',
			'width': '750',
			'height': '800'
		}

		attributes = self.array_merge(default_attributes, attributes)

		attributes_query = ''
		for attr, value in attributes.items():
			attributes_query += ' ' + str(attr) + '="' + str(value) + '"'

		return '<iframe src="' + self.get_url() + '" ' + attributes_query + '></iframe>'

	def build_controller(self, widget, flexible_call=False):
		pattern = '/^w|s|mw/'
		
		if self.get_api_type() == self.API_VC:
			if not re.search(pattern, widget):
				return self.VC_CONTROLLER
		elif self.get_api_type() == self.API_GOODS:
			if not flexible_call and not re.search(pattern, widget):
				return self.GOODS_CONTROLLER
		else:
			return self.CART_CONTROLLER

	def calculate_signature(self, params, secret, version):
		base_string = ''
		is_array = lambda var: isinstance(var, (list, tuple))

		if version == self.SIGNATURE_VERSION_1:
			base_string += params['uid'] if not self.is_empty(params, 'uid') else ''
			base_string += secret
			return self.hash(base_string, 'md5')

		else:
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
