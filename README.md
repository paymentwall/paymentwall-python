# About Paymentwall
[Paymentwall](http://paymentwall.com/?source=gh-py) is the leading digital payments platform for globally monetizing digital goods and services. Paymentwall assists game publishers, dating sites, rewards sites, SaaS companies and many other verticals to monetize their digital content and services. 
Merchants can plugin Paymentwall's API to accept payments from over 100 different methods including credit cards, debit cards, bank transfers, SMS/Mobile payments, prepaid cards, eWallets, landline payments and others. 

To sign up for a Paymentwall Merchant Account, [click here](http://paymentwall.com/signup/merchant?source=gh-py).

# Paymentwall Python Library
This library allows developers to use [Paymentwall APIs](http://paymentwall.com/en/documentation/API-Documentation/722?source=gh-py) (Virtual Currency, Digital Goods featuring recurring billing, and Virtual Cart).

To use Paymentwall, all you need to do is to sign up for a Paymentwall Merchant Account so you can setup an Application designed for your site.
To open your merchant account and set up an application, you can [sign up here](http://paymentwall.com/signup/merchant?source=gh-py).

# Installation
To install using <code>pip</code> run:

  <code>pip install paymentwall-python</code>

<b>Notice:</b> If you are using <em>Python 2.6</em> please run the following command, too:

  <code>pip install ordereddict</code>

To install from source run:

  <code>python setup.py install</code>

Then use a code sample below.

# Code Samples

## Digital Goods API

#### Initializing Paymentwall
<pre><code>from paymentwall import *
Paymentwall.set_api_type(Paymentwall.API_GOODS)
Paymentwall.set_app_key('APPLICATION_KEY') # available in your merchant area
Paymentwall.set_secret_key('SECRET_KEY') # available in your merchant area
</code></pre>

#### Widget Call
[Web API details](http://www.paymentwall.com/en/documentation/Digital-Goods-API/710#paymentwall_widget_call_flexible_widget_call)

The widget is a payment page hosted by Paymentwall that embeds the entire payment flow: selecting the payment method, completing the billing details, and providing customer support via the Help section. You can redirect the users to this page or embed it via iframe. Below is an example that renders an iframe with Paymentwall Widget.

<pre><code>product = Product(
    'product301',              # id of the product in your system 
    12.12,                     # price
    'USD',                     # currency code
    'test',                    # product name
    Product.TYPE_SUBSCRIPTION, # this is a time-based product
    1,                         # duration is 1
    Product.PERIOD_TYPE_WEEK,  #               week
    True                       # recurring
)

widget = Widget(
    'user4522',   # id of the end-user who's making the payment
    'fp',       # widget code, e.g. fp; can be picked inside of your merchant account
    [product],    # product details for Flexible Widget Call. To let users select the product on Paymentwall's end, leave this array empty
    {'email': 'user@hostname.com'}    # additional parameters
)
print(widget.get_html_code())
</code></pre>

#### Pingback Processing

The Pingback is a webhook notifying about a payment being made. Pingbacks are sent via HTTP/HTTPS to your servers. To process pingbacks use the following code:
<pre><code>pingback = Pingback({x:y for x, y in request.args.iteritems()}, request.remote_addr)

if pingback.validate():
    product_id = pingback.get_product().get_id()
    if pingback.is_deliverable():
        # deliver the product
        pass
    elif pingback.is_cancelable():
        # withdraw the product
        pass

    print('OK') # Paymentwall expects response to be OK, otherwise the pingback will be resent

else:
    print(pingback.get_error_summary())</code></pre>

## Virtual Currency API

#### Initializing Paymentwall
<pre><code>from paymentwall import *
Paymentwall.set_api_type(Paymentwall.API_VC)
Paymentwall.set_app_key('APPLICATION_KEY')
Paymentwall.set_secret_key('SECRET_KEY')
</code></pre>

#### Widget Call
<pre><code>widget = Widget(
	'user40012', # id of the end-user who's making the payment
	'p1_1',      # widget code, e.g. p1; can be picked inside of your merchant account
	[],          # array of products - leave blank for Virtual Currency API
	{'email': 'user@hostname.com'} # additional parameters
)
print(widget.get_html_code())
</code></pre>

#### Pingback Processing
<pre><code>pingback = Pingback({x:y for x, y in request.args.iteritems()}, request.remote_addr)
if pingback.validate():
    virtual_currency = pingback.get_vc_amount()
    if pingback.is_deliverable():
        # deliver the virtual currency
        pass
    elif pingback.is_cancelable():
        # withdraw the virtual currency
        pass 
  print('OK') # Paymentwall expects response to be OK, otherwise the pingback will be resent
else:
  print(pingback.get_error_summary())
end</code></pre>

## Cart API

#### Initializing Paymentwall
<pre><code>from paymentwall import *
Paymentwall.set_api_type(Paymentwall.API_CART)
Paymentwall.set_app_key('APPLICATION_KEY')
Paymentwall.set_secret_key('SECRET_KEY')
</code></pre>

#### Widget Call
<pre><code>widget = Widget(
	'user40012', # id of the end-user who's making the payment
	'p1_1',      # widget code, e.g. p1; can be picked inside of your merchant account
	[
		Product('product301', 3.33, 'EUR'), # first product in cart
		Product('product607', 7.77, 'EUR')  # second product in cart
	],
	{'email': 'user@hostname.com'} # additional params
)
print(widget.get_html_code())</code></pre>

#### Pingback Processing
<pre><code>pingback = Pingback({x:y for x, y in request.args.iteritems()}, request.remote_addr)
if pingback.validate():
    products = pingback.get_products()
    if pingback.is_deliverable():
        # deliver the virtual currency
        pass
    elif pingback.is_cancelable():
        # withdraw the virtual currency
        pass 
  print('OK') # Paymentwall expects response to be OK, otherwise the pingback will be resent
else:
  print(pingback.get_error_summary())
end</code></pre>
