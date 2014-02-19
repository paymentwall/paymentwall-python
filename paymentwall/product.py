class Product:

	TYPE_SUBSCRIPTION = 'subscription'
	TYPE_FIXED = 'fixed'

	PERIOD_TYPE_DAY = 'day'
	PERIOD_TYPE_WEEK = 'week'
	PERIOD_TYPE_MONTH = 'month'
	PERIOD_TYPE_YEAR = 'year'

	def __init__(
				self, product_id=None, amount=0.0, currency_code=None, name=None, product_type=TYPE_FIXED, period_length=0,
				period_type=None, recurring=False, trial_product=object):
		self.product_id = product_id
		self.amount = round(amount, 2)
		self.currency_code = currency_code
		self.name = name
		self.product_type = product_type
		self.period_length = period_length
		self.period_type = period_type
		self.recurring = recurring
		self.trial_product = trial_product if self.TYPE_SUBSCRIPTION and recurring and recurring != 0 else None

	def get_id(self):
		return self.product_id

	def get_amount(self):
		return self.amount

	def get_currency_code(self):
		return self.currency_code

	def get_name(self):
		return self.name

	def get_type(self):
		return self.product_type

	def get_period_type(self):
		return self.period_type

	def get_period_length(self):
		return self.period_length

	def is_recurring(self):
		return self.recurring

	def get_trial_product(self):
		return self.trial_product