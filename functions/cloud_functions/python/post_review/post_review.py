import sys
import os
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from dotenv import load_dotenv

# Load environment variables and assign them to variables
# load_dotenv("../.env")

def main(dict):
    print(dict)
    authenticator = IAMAuthenticator(os.getenv('IAM_API_KEY'))
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(os.getenv('COUCH_URL'))
    response = service.post_document(db='reviews', document=dict["review"]).get_result()
    print("Response: ", response)
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