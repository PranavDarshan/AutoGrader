import faiss
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import fitz
import numpy as np
import matplotlib.pyplot as plt

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
    embedding_function=hf_embeddings.embed_query  # or embed_documents based on your use case
)

def context(query):
    try:
        # Perform similarity search
        query_results = library.similarity_search(query)
        
        if not query_results:
            print("No results found for the query.")
            return None
        
        top_result = query_results[0]
        pdf_path = "os tb.pdf"
        
        # Open the PDF
        doc = fitz.open(pdf_path)
        page_number = top_result.metadata.get('page', 0)
        page = doc.load_page(page_number)
        
        # Get image from the PDF page
        img = page.get_pixmap(dpi=300)
        doc.close()

        # Convert the pixmap to a numpy array
        img_array = np.frombuffer(img.samples, dtype=np.uint8).reshape((img.height, img.width, img.n))
        
        # Display the image using matplotlib
        plt.figure(figsize=(13, 10))
        plt.imshow(img_array)
        plt.axis("off")
        plt.show()

        return top_result.page_content[15:]
    
    except Exception as e:
        print(f"Error processing query: {e}")
        return None

# Example query
result = context("What are real-time systems?")
if result:
    print(result)
else:
    print("No content found or an error occurred.")
