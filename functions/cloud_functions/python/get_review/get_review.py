import sys
import os
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from dotenv import load_dotenv

# Load environment variables and assign them to variables
# load_dotenv()

# Initialize variables from environment variables
IAM_API_KEY = os.getenv('IAM_API_KEY')
COUCH_URL = os.getenv('COUCH_URL')

# Check if the environment variables are loaded
# print(IAM_API_KEY)
# print(COUCH_URL)

# Define main function
def main(dict):
    print("parameters:", dict)
    authenticator = IAMAuthenticator(IAM_API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(COUCH_URL)
    response = service.post_find(
                db='reviews',
                selector={'dealership': {'$eq': int(dict['id'])}},
            ).get_result()
    try: 
        # result_by_filter=my_database.get_query_result(selector,raw_result=True) 
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response} 
            }        
        return result
    except:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
            }

