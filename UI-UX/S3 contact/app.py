from flask import Flask, request, jsonify, render_template, redirect, url_for
import boto3
import json
import os
import time

app = Flask(__name__)

# AWS credentials and configuration
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_REGION = 'your-region'
S3_BUCKET = 'your-bucket-name'

# Initialize the S3 client
s3_client = boto3.client('s3', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID, 
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                         region_name=AWS_REGION)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_to_s3():
    json_data = request.form.get('json_data')
    
    if not json_data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        data = json.loads(json_data)
    except ValueError as e:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Generate a unique file name (you can customize this as needed)
    file_name = f"data_{int(time.time())}.json"

    try:
        # Upload JSON data to S3 bucket
        s3_client.put_object(Bucket=S3_BUCKET, Key=file_name, Body=json_data)
        return jsonify({"message": "File uploaded successfully", "file_name": file_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
