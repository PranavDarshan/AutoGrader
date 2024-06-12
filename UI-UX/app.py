import os
from flask import Flask, request, render_template
from google.cloud import vision
from werkzeug.utils import secure_filename
import faiss
import pickle
import base64
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import fitz
import numpy as np
import matplotlib.pyplot as plt
import io
import requests
import json
api_url = "https://duddx53ro1.execute-api.us-east-1.amazonaws.com/dev/sagemaker"

# Set the environment variable for Google Cloud Vision API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_ocr.json.json'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def detect_text(path):
    client = vision.ImageAnnotatorClient()
    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    # finalstr2 = texts[0].description + " evaluate this answer from 1-5 be conservative while giving the marks"    
    return requests.post(api_url, json={"input_text": texts[0].description+'\\evaluate this answer given by the user with reference to the question and give a score from 1-5 and be conseravtive in giving marks'}).json()
    

# def extract_score_and_explanation(format_str):
#     # Load JSON data from the file
#     # Extract the score and explanation from the JSON data
#     score = None
#     explanation = None
    
    
    
#     score_start = format_str.find("Score:")
#     score_end = format_str.find("/5", score_start)
#     if score_start != -1 and score_end != -1:
#         score_text = format_str[score_start:score_end+2]
#         score = score_text.strip()
    
#     explanation_start = format_str.find("Explanation:")
#     if explanation_start != -1:
#         explanation = format_str[explanation_start+13:].strip()
    
#     return score + explanation

# Load the FAISS index
index_path = "faiss_index1.bin"
try:
    index = faiss.read_index(index_path)
except Exception as e:
    print(f"Error loading FAISS index from {index_path}: {e}")
    raise

# Load the metadata
metadata_path = "faiss_metadata1.pkl"
try:
    with open(metadata_path, "rb") as f:
        docstore, index_to_docstore_id = pickle.load(f)
except Exception as e:
    print(f"Error loading metadata from {metadata_path}: {e}")
    raise

# Set up HuggingFace embeddings
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Initialize the FAISS library
library = FAISS(
    index=index,
    docstore=docstore,
    index_to_docstore_id=index_to_docstore_id,
    embedding_function=hf_embeddings.embed_query
)

def get_pdf_page_image(query):
    try:
        query_results = library.similarity_search(query)
        if not query_results:
            return None, None
        top_result = query_results[0]
        pdf_path = "os tb.pdf"
        doc = fitz.open(pdf_path)
        page_number = top_result.metadata.get('page', 0)
        page = doc.load_page(page_number)
        img = page.get_pixmap(dpi=300)
        doc.close()

        img_array = np.frombuffer(img.samples, dtype=np.uint8).reshape((img.height, img.width, img.n))
        fig, ax = plt.subplots(figsize=(13, 10))
        ax.imshow(img_array)
        ax.axis("off")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        return top_result.page_content[15:], buf

    except Exception as e:
        print(f"Error processing query: {e}")
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    ocr_text = None
    result_text = None
    image_data = None
    
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            ocr_text = detect_text(filepath)
        
        # Handle text query
        if 'query' in request.form and request.form['query'].strip() != '':
            query = request.form['query']
            result_text, image_buf = get_pdf_page_image(query)
            if image_buf:
                image_data = 'data:image/png;base64,' + base64.b64encode(image_buf.read()).decode('utf-8')
    
    return render_template('index.html', ocr_text=ocr_text, result_text=result_text, image_data=image_data)

if __name__ == '__main__':
    app.run(debug=True)
