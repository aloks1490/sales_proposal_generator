import streamlit as st
import os
from rag_engine import ProposalRAG
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader

st.set_page_config(page_title="Local Proposal Gen", layout="wide")

st.title("AI Proposal Generator")
# st.markdown("Path A: Fully Local (Ollama + Chroma)")

# Initialize Engine
if 'rag' not in st.session_state:
    st.session_state.rag = ProposalRAG()

with st.sidebar:
    st.header("1. Upload Context")
    uploaded_files = st.file_uploader("Upload Company PDF/TXT/DOCX", accept_multiple_files=True)
    
    st.header("2. Meeting Context")
    meeting_notes = st.text_area("Paste Meeting Notes / Transcription here", height=200)

# Main Prompt Area
user_instr = st.text_input("Specific instructions?", placeholder="e.g. Focus on ROI and sustainability")

if st.button("Generate Proposal"):
    if not uploaded_files or not meeting_notes:
        st.error("Please provide both context files and meeting notes.")
    else:
        with st.spinner("Processing documents and thinking..."):
            # Load docs
            all_docs = []
            for uploaded_file in uploaded_files:
                temp_path = f"./uploads/{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                if temp_path.endswith(".pdf"):
                    loader = PyPDFLoader(temp_path)
                elif temp_path.endswith(".docx"):
                    loader = UnstructuredWordDocumentLoader(temp_path)
                else:
                    loader = TextLoader(temp_path)
                all_docs.extend(loader.load())

            # Index & Generate
            st.session_state.rag.process_documents(all_docs)
            proposal = st.session_state.rag.generate_proposal(user_instr, meeting_notes)
            
            st.markdown("---")
            st.subheader("Generated Proposal")
            st.markdown(proposal)
            
            st.download_button("Download Markdown", proposal, file_name="proposal.md")