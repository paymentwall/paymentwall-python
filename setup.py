import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name='paymentwall-python',
	version='1.0.7',
	packages=['paymentwall'],
	url='https://github.com/paymentwall/paymentwall-python',
	description='Paymentwall Python Library',
	long_description=read('pypi_description.rst'),
	license='MIT',
	author='Paymentwall Team',
	author_email='devsupport@paymentwall.com'
)
