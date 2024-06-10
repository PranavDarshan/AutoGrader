import os
import json
import boto3


# Get environment variables
ENDPOINT_NAME = os. environ[' ENDPOINT_NAME']


def lambda_handler(event, context):

  # Extract query from the event
  query = event['input_text'] # Assuming query is in the body
  # Use Boto3 to invoke SageMaker endpoint
  runtime = boto3. client('runtime.sagemaker')
  
  response = runtime.invoke_endpoint(
      EndpointName = ENDPOINT_NAME,
      ContentType = 'application/json',
      Body = json.dumps (['inputs': query}) - encode()
  )
  
  # Decode and return the model output
  output = json.loads(response['Body'].read().decode())
  return {
    "statusCode": 200,
    "body": json.dumps (output)
  }
