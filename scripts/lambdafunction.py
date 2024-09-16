import time
import base64
import logging
import json
import boto3
#import numpy

# Set logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

print('Loading Lambda function')

runtime = boto3.Session().client('sagemaker-runtime')
endpoint_name = "pytorch-inference-2024-09-13-17-54-57-301" #changes for every generated endpoint

# Define the labda function itself
def lambda_handler(event, context):
    #x = event['content']
    #aa = x.encode('ascii')
    #bytes = base64.b64decode(aa)
    start_time = time.time()

    print('Context:::', context)
    print('EventType::', type(event))
    bytes = event
    runtime = boto3.Session().client('sagemaker-runtime')
    
    response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                    ContentType="application/json",
                                    Accept='application/json',
                                    #Body=bytearray(x)
                                    Body=json.dumps(bytes))
    
    #result = response["Body"].read().decode('utf-8')
    #sss=json.loads(result)
    result = json.loads(response["Body"].read().decode("utf-8"))

    end_time = time.time()
    exec_time = end_time - start_time
    logger.info(f"Execution time: {exec_time:.4f} seconds.")
    
    return {
        "statusCode": 200,
        'headers' : {"Content-Type" : "text/plain", "Access-Control-Allow-Origin" : "*" },
        "type-result": str(type(result)),
        "COntent-Type-In": str(context),
        "body" : json.dumps(result)
        }
