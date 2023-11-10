import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        # Call post method of requests library with URL, json_payload and parameters
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occured")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url)
    if dealers:
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# get_dealer_by_id_from_cf function uses ibm cloud function to get dealer by id
def get_dealer_by_id_from_cf(url, dealer_id):
    dealer = get_request(url, id=dealer_id)
    if dealer:
        # Create a CarDealer object with values in `dealer` object
        return CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                         id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                         short_name=dealer["short_name"],
                         st=dealer["st"], zip=dealer["zip"])

# get_dealer_by_state_from_cf function uses ibm cloud function to get a list of dealers by state
def get_dealer_by_state_from_cf(url, state):
    results = []
    dealers = get_request(url, st=state)
    print("dealers by state list:")
    print(dealers)
    print("")
    if dealers:
        # Iterate through dealers list
        for dealer in dealers:
            print("Dealer from state:")
            print(dealer)
            print("")
            # Create CarDealer object with values from `dealer` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
        return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []    
    dealers = get_request(url, id=dealer_id)
    if dealers:
        print("The following is a dealers object")
        print(dealers)
        # Get list from docs
        review_docs = dealers["data"]["docs"]
        # iterate through list of reviews
        for review in review_docs:
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                      review=review["review"], purchase_date=review["purchase_date"], 
                                      car_make=review["car_make"], car_model=review["car_model"], 
                                      car_year=review["car_year"], sentiment="sentiment", id=review["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
        return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/0ceb5f31-171b-4349-a43a-e2d614cf7c12'
    api_key = 'UzDmjIBquw_tVIll1ZCUKShB83FsbT9s0A-P_kGeBV1G'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text=dealer_review, features=Features(sentiment=SentimentOptions(targets=[dealer_review]))).get_result()
    label = response['sentiment']['document']['label']
    return label