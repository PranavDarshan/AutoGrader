# Deploying the Fine Tuned Llama2 on AWS SageMaker

Since this model is a very large model and cannot be run on the local machine we make use of AWS Sagemaker to deploy this model. We tried to run this model locally on computers having <b>NVIDIA RTX 4050 GPU with 6GB</b> of memory. But this was still not enough to run the Llama2 model.

# Architecture 

<img src=https://github.com/PranavDarshan/AutoGrader/blob/main/assets/aws_auto.png/>

# Step 1: Pull the Model from HuggingFace

The model which was published to HuggingFace by the colab notebook now needs to be pulled to AWS Sagemaker for deployment.The link can be used to get the code for model deployment : https://huggingface.co/NiharMandahas/Os_script_evaluator. 

![image](https://github.com/PranavDarshan/AutoGrader/assets/65911046/b59d6571-9176-42f3-9ba6-4ec1401621c8)


1. Create a new jupyter notebook instance and paste the code in [sagemaker.ipynb](https://github.com/PranavDarshan/AutoGrader/blob/main/AWS-Deployment/sagemaker.ipynb) and run all the cells.
2. In the predictor, give different inputs and check the output if it is working.

# Step 2: Create an Endpoint 

Navigate to the endpoints feild in the left navigation tab

<img src=https://github.com/PranavDarshan/AutoGrader/blob/main/assets/endpoint_creation.png>

Create an endpoint by adding a model. The model selected to be deployed is present under deployable models.

# Step 3: Create a Lambda Function 

Create a Lambda Function to Access the SageMaker Endpoint from the internet. For this we will need to create a Lambda function and with the code given in in the [lambda_func.py](https://github.com/PranavDarshan/AutoGrader/blob/main/AWS-Deployment/lambda_func.py). Test the Lambda function by giving the input as 

```
{
  "input_text": "Question:What is caching? Answer:Paging is a technique of memery management. \\evaluate this answer given by the user with reference to the question and give a score from 1-5 and be conseravtive in giving marks"
}
```
Create a trigger for the Lambda Function using a REST API so that whenever this a POST request is done on this API, Lambda function passes this data to the model. 

<img src=https://github.com/PranavDarshan/AutoGrader/blob/main/assets/lambda_func.jpg>

# Step 4: Create a REST API Trigger for Lambda Function

1. Navigate to the AWS API Gateway service
2. Create a REST API trigger with POST request and copy the invoke URL. This method can also be tested by the help of the test option in the API Gateway.

<img src=https://github.com/PranavDarshan/AutoGrader/blob/main/assets/api_gateway.jpg>

Use the invoke URL for integration in the UI/UX part. 

<b>Remember to not give any authorization key or token while creating the API. This will make it harder for us to integrate with our website.</b>
