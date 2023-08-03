from bottle import *
import os, stripe

os.chdir(os.path.dirname(os.path.abspath(__file__)))

stripe.api_key=os.getenv('STRIPE_API_KEY')
stripe.api_version="2022-11-15"

@route('/')
def index():
  logged_in_email=request.headers.get('X-Forwarded-Email') or None

  stripe_customer=None
  stripe_subscriptions=None
  
  if (logged_in_email):
    search_result=stripe.Customer.search(
      query='email: "' + logged_in_email +'"',
      limit=1
    )
  
    if (search_result.has_more):
      return view("Unexpectedly Had More than 1 Customer Result")
  
  if (len(search_result.data) == 1):
    stripe_customer=search_result.data[0]
    
    stripe_subscriptions=stripe.Subscription.list(customer=stripe_customer.id, limit=100)
    if (stripe_subscriptions.has_more):
      return view("Unexpectedly Had More than 100 Subscription Results")
  
  return template('templates/index.html',
    headers=request.headers,
    logged_in_email=logged_in_email,
    stripe_customer=stripe_customer,
    stripe_subscriptions=stripe_subscriptions
  )

run(host='0.0.0.0', port=8080)

