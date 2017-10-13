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

## Widget API - Digital Goods

#### Initializing Paymentwall
<pre><code>from paymentwall import *
Paymentwall.set_api_type(Paymentwall.API_GOODS)
Paymentwall.set_app_key('APPLICATION_KEY') # available in your merchant area
Paymentwall.set_secret_key('SECRET_KEY') # available in your merchant area
</code></pre>

#### Widget Call
[Web API details](https://docs.paymentwall.com/integration/widget/digital-goods)

The widget is a payment page hosted by Paymentwall that embeds the entire payment flow: selecting the payment method, completing the billing details, and providing customer support via the Help section. You can redirect the users to this page or embed it via iframe. Below is an example that renders an iframe with Paymentwall Widget.

<pre><code>
widget = Widget(
    'user4522',   # id of the end-user who's making the payment
    'pw',       # widget code, e.g. pw; can be picked inside of your merchant account
    [],    # To let users select the product on Paymentwall's end, leave this array empty
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

## Widget API - Virtual Currency

#### Initializing Paymentwall
<pre><code>from paymentwall import *
Paymentwall.set_api_type(Paymentwall.API_VC)
Paymentwall.set_app_key('APPLICATION_KEY')
Paymentwall.set_secret_key('SECRET_KEY')
</code></pre>

#### Widget Call
[Web API details](https://docs.paymentwall.com/integration/widget/virtual-currency)
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

## Widget API - Cart

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

## Checkout API

#### Initializing Paymentwall
<pre><code>from paymentwall import *
Paymentwall.set_api_type(Paymentwall.API_CHECKOUT)
Paymentwall.set_app_key('APPLICATION_KEY') # available in your merchant area
Paymentwall.set_secret_key('SECRET_KEY') # available in your merchant area
</code></pre>

#### Widget Call
[Web API details](https://docs.paymentwall.com/integration/checkout-home)

The widget is a payment page hosted by Paymentwall that embeds the entire payment flow: selecting the payment method, completing the billing details, and providing customer support via the Help section. You can redirect the users to this page or embed it via iframe. Below is an example that renders an iframe with Paymentwall Widget.

<pre><code>product = Product(
    'product301',              # id of the product in your system
    12.12,                     # price
    'USD',                     # currency code
    'test',                    # product name
    Product.TYPE_SUBSCRIPTION, # this is a time-based product
    1,                         # duration is 1
    Product.PERIOD_TYPE_WEEK,  # week
    True                       # recurring
)

widget = Widget(
    'user4522',   # id of the end-user who's making the payment
    'pw',       # widget code, e.g. pw; can be picked inside of your merchant account
    [product],    # product details for Flexible Widget Call. To let users select the product on Paymentwall's end, leave this array empty
    {
        'email': 'user@hostname.com', # email of user
        'ps':'all' # shortcode of the payment option
    }
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

## Brick API
[Web API details](https://docs.paymentwall.com/integration/direct/brick-home)

#### Create a one-time token
<pre><code>
url = 'https://api.paymentwall.com/api/brick/token'
data_request = {
    'public_key': 'YOUR_PUBLIC_KEY',
    'card[number]':'4242424242424242',
    'card[exp_month]':'11',
    'card[exp_year]':'21',
    'card[cvv]':'123',
}
#headers = {'X-ApiKey': 'YOUR_PRIVATE_KEY'}

r = requests.post(url, data=data_request) # send post request
response = json.loads(r.text) # get response in json
token = response['token']
</code></pre>

#### Charge
<pre><code>
url = 'https://api.paymentwall.com/api/brick/charge'
data_request = {
    # if generate via brick.js
    # 'token':request.POST['brick_token']
    # if generate via backend
    'token':token
    'fingerprint':request.POST['brick_fingerprint'],
    'amount': 1,
    'currency':'USD',
    'description':'Test Order',
    'email':'test@gmail.com',
    'customer[firstname]':'Test',
    'customer[lastname]':'User'
}
headers = {'X-ApiKey': 'YOUR_PRIVATE_KEY'}

r = requests.post(url, data=data_request, headers=headers) # send post request
response = json.loads(r.text) # get response in json
</code></pre>

#### Charge - refund
<pre><code>
url = 'https://api.paymentwall.com/api/brick/charge/charge_id/refund'
data_request = {}
headers = {'X-ApiKey': 'YOUR_PRIVATE_KEY'}

r = requests.post(url, data=data_request, headers=headers) # send post request
response = json.loads(r.text) # get response in json
</code></pre>

#### Subscription
<pre><code>
url = 'https://api.paymentwall.com/api/brick/subscription'
data_request = {'amount': 1,
    # if generate via brick.js
    # 'token':request.POST['brick_token']
    # if generate via backend
    'token':token
    'fingerprint':request.POST['brick_fingerprint'],
    'currency':'USD',
    'description':'Test Order',
    'email':'michael@paymentwall.com',
    'plan':'Test Plan',
    'period':'month',
    'period_duration':1
    # if trial, add following parameters
    'trial[amount]':1,
    'trial[currency]':'USD',
    'trial[period]':'month',
    'trial[period_duration]:1'
}
headers = {'X-ApiKey': 'YOUR_PRIVATE_KEY'}

r = requests.post(url, data=data_request, headers=headers) # send post request
response = json.loads(r.text) # get response in json
</code></pre>

#### Subscription - cancel
<pre><code>
url = 'https://api.paymentwall.com/api/brick/subscription/subscription_id/cancel'
data_request = {}
headers = {'X-ApiKey': 'YOUR_PRIVATE_KEY'}

r = requests.post(url, data=data_request, headers=headers) # send post request
response = json.loads(r.text) # get response in json
</code></pre>

## Mobiamo API
[Web API details](https://docs.paymentwall.com/integration/direct/mobiamo-home)

#### Initiate Paymentwall
<pre><code>from paymentwall import *
Paymentwall.set_app_key('YOUR_PROJECT_KEY')
Paymentwall.set_secret_key('YOUR_SECRET_KEY')
</code></pre>

#### Get a token
<pre><code>
url = 'https://api.paymentwall.com/api/mobiamo/token'
data_request = {
    'key':'YOUR_PROJECT_KEY',
    'uid':'test', # User ID in your system
    'sign_version':3, # Signature version, can be 2 or 3
    'ts':int(time.time())
}
data_request['sign'] = Paymentwall.request_calculate_signature(data_request,Paymentwall.get_secret_key(),data_request['sign_version'])

r = requests.post(url, data=data_request) # send post request
response = json.loads(r.text) # get response in json
token = response['token']
</code></pre>

#### Initiate payment
<pre><code>
url = 'https://api.paymentwall.com/api/mobiamo/init-payment'
data_request = {
    'key':'YOUR_PROJECT_KEY',
    'uid':'test',
    'amount':2000,
    'currency':'PHP', # currency code of the payment
    'country':'PH', # country code of the payment
    'product_id':'product101', # ID of the order in your system
    'product_name':'Test Product', # Name of the order
    'carrier':'255' # mandatory in some countries - ID of the mobile operator
}

headers = {'Token':token} # Token returned from get token request

r = requests.post(url,data=data_request,headers=headers) # send post request
response = json.loads(r.text) # get response in json
</code></pre>

#### Process payment
<pre><code>
url = 'https://api.paymentwall.com/api/mobiamo/process-payment'
data_request = {
    'key':'YOUR_PROJECT_KEY',
    'uid':'test',
    'ref':'w129548784', # reference id of the payment, returned from initiate payment request
    'flow':'msisdn', # flow returned from initiate payment request
    'data':'6312345678' # value can be: code user received after sending message OR phone number of user
}
headers = {'Token':token}

r = requests.post(url,data=data_request,headers=headers) # send post request
response = json.loads(r.text) # get response in json
</code></pre>