from bottle import Bottle, request, template, redirect
import os, stripe, requests, json, logging, jwt

logging.basicConfig(level=logging.INFO)

log = logging.getLogger()
app = Bottle()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

stripe.api_key=os.getenv('STRIPE_API_SECRET_KEY')
stripe.api_version="2022-11-15"

@app.route('/')
def index():
  log.debug("debug log")
  log.info("info log")
  log.warning("warning log")
  log.error("error log")

  jwt_token=request.headers.get('Authorization').replace('Bearer ', '') if 'Authorization' in request.headers else None
  try:
    auth=jwt.decode(jwt_token, options={"verify_signature": False}) if jwt_token else None
    log.info("Auth: %s", auth)
  except Exception as e:
    log.error("Error parsing jwt_token: %s", jwt_token)
    log.exception(e)
    auth=None
    # return redirect('/oauth2/sign_out')
    
  logged_in_email=request.headers.get('X-Forwarded-Email') or None
  
  if (not logged_in_email):
    if (os.getenv('UNSAFE_ALLOW_QUERY_PARAM_EMAIL')):
      logged_in_email=request.query.get('email')

  stripe_customer=None
  stripe_subscriptions=None
  
  if (logged_in_email):
    search_result=stripe.Customer.list(email=logged_in_email, limit=1)
  
    if (search_result.has_more):
      return "Unexpectedly Had More than 1 Customer Result"

    if (len(search_result.data) > 0):
      stripe_customer=search_result.data[0]
      
      stripe_subscriptions=stripe.Subscription.list(customer=stripe_customer.id, limit=100)
      if (stripe_subscriptions.has_more):
        return "Unexpectedly Had More than 100 Subscription Results"
  
  return template('templates/index.html',
    headers=request.headers,
    auth=auth,
    logged_in_email=logged_in_email,
    stripe_customer=stripe_customer,
    stripe_subscriptions=stripe_subscriptions,
    stripe_api_public_key=os.getenv('STRIPE_API_PUBLIC_KEY')
  )

@app.route('/hello')
def index():
  return "hello"

@app.route('/public/email_verification')
def index():
  return 'Your email '+request.query.get('email', '')+' isn\'t verified yet. <a href="/oauth2/sign_in?rd=/hello">Try again</a> (select forgot password if you need a new verification link)';

app.run(host='0.0.0.0', port=8080)

