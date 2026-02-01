import os
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    UnstructuredWordDocumentLoader
)

def load_uploaded_files(file_list):
    """
    Takes a list of Streamlit UploadedFile objects, 
    saves them temporarily, and loads their content.
    """
    documents = []
    
    # Ensure uploads directory exists
    if not os.path.exists("./uploads"):
        os.makedirs("./uploads")

    for uploaded_file in file_list:
        file_path = os.path.join("./uploads", uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Determine which loader to use based on extension
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".docx") or file_path.endswith(".doc"):
            loader = UnstructuredWordDocumentLoader(file_path)
        elif file_path.endswith(".txt") or file_path.endswith(".md"):
            loader = TextLoader(file_path)
        else:
            continue
            
        documents.extend(loader.load())
    
    return documents