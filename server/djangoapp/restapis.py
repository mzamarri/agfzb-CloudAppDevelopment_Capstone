import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions


def get_request(url, **kwargs):
    # Initialize response with a default value
    response = None
    
    # If argument contains API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of the requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except Exception as e:
        # Handle the exception and print the error message
        print(f"Network exception occurred: {e}")
        # Optionally, you can raise the exception to propagate it further
        raise e

    if response is not None:
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(json_payload)

    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result and isinstance(json_result, list):
        # Check if the JSON result is a list
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
           
                # Check if the dealer is a dictionary with a "doc" key
            dealer_doc = dealer
            print(dealer_doc)
                # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                    address=dealer_doc.get("address", ""),
                    city=dealer_doc.get("city", ""),
                    full_name=dealer_doc.get("full_name", ""),
                    id=dealer_doc.get("id", ""),
                    lat=dealer_doc.get("lat", ""),
                    long=dealer_doc.get("long", ""),
                    short_name=dealer_doc.get("short_name", ""),
                    st=dealer_doc.get("st", ""),
                    zip=dealer_doc.get("zip", "")
                )
            results.append(dealer_obj)

    return results



def get_dealer_by_id_from_cf(url, id):
    results = []
    json_result = get_request(url, id=id)
    
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer
            if dealer_doc["id"] == id:
                dealer_obj = CarDealer(
                    address=dealer_doc["address"],
                    city=dealer_doc["city"],
                    full_name=dealer_doc["full_name"],
                    id=dealer_doc["id"],
                    lat=dealer_doc["lat"],
                    long=dealer_doc["long"],
                    short_name=dealer_doc["short_name"],
                    st=dealer_doc["st"],
                    zip=dealer_doc["zip"]
                )
                results.append(dealer_obj)

    # Check if there are results before returning
    if results:
        return results[0]
    else:
        return None

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    
    if json_result and "data" in json_result and "docs" in json_result["data"]:
        reviews = json_result["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review.get("dealership", ""),
                                      name=dealer_review.get("name", ""),
                                      purchase=dealer_review.get("purchase", False),
                                      review=dealer_review.get("review", ""))
            review_obj.id = dealer_review.get("id", "")
            review_obj.purchase_date = dealer_review.get("purchase_date", "")
            review_obj.car_make = dealer_review.get("car_make", "")
            review_obj.car_model = dealer_review.get("car_model", "")
            review_obj.car_year = dealer_review.get("car_year", "")
            
            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://de31a4d0-0714-4cfb-afd1-462dc8749635-bluemix.cloudantnosqldb.appdomain.cloud"
    api_key = "64NzpP_9Q7xDpNI87mIepUDR06WUSgHSdfnR6HSNWB54"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    
    return(label)
