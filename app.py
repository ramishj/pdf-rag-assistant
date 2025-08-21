import streamlit as st
import os
import tempfile
from pathlib import Path
import PyPDF2
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
import json
from datetime import datetime
import base64
import uuid
import re

# Set environment variable to avoid tokenizers warning
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# LLM Provider imports
import openai
import anthropic
import google.generativeai as genai
from openai import AzureOpenAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Page configuration
st.set_page_config(
    page_title="PDF Knowledge Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #111827;
    }
    .main .block-container {
        background-color: #111827;
    }
    .stSidebar {
        background-color: #1f2937;
    }
    .stTextInput > div > div > input {
        background-color: #374151;
        color: #f9fafb;
        border-color: #4b5563;
    }
    .stSelectbox > div > div > div {
        background-color: #374151;
        color: #f9fafb;
    }
    .stSlider > div > div > div > div {
        background-color: #374151;
    }
</style>
""", unsafe_allow_html=True)

# Modern CSS with gradients, shadows, and animations
st.markdown("""
<style>
    /* Modern CSS Reset and Base Styles */
    * {
        box-sizing: border-box;
    }
    
    /* Custom CSS Variables */
    :root {
        --primary-color: #6366f1;
        --primary-dark: #4f46e5;
        --secondary-color: #8b5cf6;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --bg-primary: #1f2937;
        --bg-secondary: #111827;
        --bg-tertiary: #374151;
        --border-color: #4b5563;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.4);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5), 0 4px 6px -4px rgb(0 0 0 / 0.5);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.6), 0 8px 10px -6px rgb(0 0 0 / 0.6);
    }
    
    /* Modern Header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        text-shadow: var(--shadow-lg);
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Modern Cards */
    .modern-card {
        background: var(--bg-primary);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-color);
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: 16px 16px 0 0;
    }
    
    /* Upload Area */
    .upload-area {
        border: 3px dashed var(--primary-color);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-area:hover {
        border-color: var(--secondary-color);
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        transform: scale(1.02);
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Chat Messages */
    .chat-container {
        background: var(--bg-secondary);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
    }
    
    .chat-message {
        padding: 1.25rem;
        border-radius: 16px;
        margin: 1rem 0;
        position: relative;
        animation: slideInRight 0.5s ease-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        margin-left: 2rem;
        border-radius: 20px 20px 4px 20px;
        box-shadow: var(--shadow-md);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        color: var(--text-primary);
        margin-right: 2rem;
        border-radius: 20px 20px 20px 4px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-md);
    }
    
    .message-timestamp {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        display: block;
    }
    
    /* Document Management */
    .document-item {
        background: var(--bg-primary);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .document-item:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow-md);
    }
    
    /* Action Buttons */
    .action-btn {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
        color: var(--text-primary);
    }
    
    .action-btn:hover {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
        transform: scale(1.05);
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    .status-active {
        background: var(--success-color);
    }
    
    .status-processing {
        background: var(--warning-color);
    }
    
    .status-error {
        background: var(--error-color);
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .document-actions {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        display: flex;
        gap: 0.5rem;
    }
    
    .action-btn {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .action-btn:hover {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }
    
    .remove-btn {
        background: var(--error-color);
        color: white;
        border-color: var(--error-color);
    }
    
    .remove-btn:hover {
        background: #dc2626;
        border-color: #dc2626;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid var(--border-color);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgb(99 102 241 / 0.1);
    }
    
    /* Select Boxes */
    .stSelectbox > div > div > div {
        border-radius: 12px;
        border: 2px solid var(--border-color);
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgb(99 102 241 / 0.1);
    }
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background: var(--primary-color);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    .status-active {
        background: var(--success-color);
    }
    
    .status-processing {
        background: var(--warning-color);
    }
    
    .status-error {
        background: var(--error-color);
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: 10px;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .modern-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .upload-area {
            padding: 2rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_pdfs' not in st.session_state:
    st.session_state.uploaded_pdfs = []
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None
if 'embeddings_model' not in st.session_state:
    st.session_state.embeddings_model = None
if 'current_collection' not in st.session_state:
    st.session_state.current_collection = None

class PDFProcessor:
    def __init__(self):
        self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        return chunks
    
    def create_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """Create embeddings for text chunks"""
        return self.embeddings_model.encode(chunks).tolist()

class VectorDatabase:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = None
    
    def create_collection(self, name: str):
        """Create a new collection for PDF documents"""
        try:
            self.collection = self.client.create_collection(name=name)
            return True
        except:
            self.collection = self.client.get_collection(name=name)
            return True
    
    def add_documents(self, chunks: List[str], embeddings: List[List[float]], metadata: List[Dict]):
        """Add document chunks to the vector database"""
        if self.collection:
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadata,
                ids=[f"chunk_{i}" for i in range(len(chunks))]
            )
    
    def search_similar(self, query: str, embeddings_model, n_results: int = 5):
        """Search for similar documents"""
        if self.collection:
            query_embedding = embeddings_model.encode([query]).tolist()
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            return results
        return None
    
    def remove_document(self, filename: str):
        """Remove all chunks for a specific document"""
        if self.collection:
            try:
                # Get all documents and find chunks to remove
                all_data = self.collection.get()
                chunks_to_remove = []
                
                for i, metadata in enumerate(all_data['metadatas']):
                    if metadata and metadata.get('filename') == filename:
                        chunks_to_remove.append(all_data['ids'][i])
                
                if chunks_to_remove:
                    self.collection.delete(ids=chunks_to_remove)
                    return True
            except Exception as e:
                st.error(f"Error removing document: {str(e)}")
        return False

class LLMProvider:
    def __init__(self, provider: str, api_key: str, model: str = None, azure_endpoint: str = None):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.azure_endpoint = azure_endpoint
        self.client = None
        self.setup_client()
    
    def setup_client(self):
        """Setup the LLM client based on provider"""
        try:
            if self.provider == "OpenAI":
                openai.api_key = self.api_key
                self.client = ChatOpenAI(
                    openai_api_key=self.api_key,
                    model_name=self.model or "gpt-3.5-turbo",
                    temperature=0.7
                )
            elif self.provider == "Claude":
                self.client = ChatAnthropic(
                    anthropic_api_key=self.api_key,
                    model_name=self.model or "claude-3-sonnet-20240229"
                )
            elif self.provider == "Azure":
                # Use Azure OpenAI client directly
                self.client = AzureOpenAI(
                    api_version="2024-12-01-preview",
                    azure_endpoint=self.azure_endpoint,
                    api_key=self.api_key,
                )
            elif self.provider == "Grok":
                genai.configure(api_key=self.api_key)
                self.client = ChatGoogleGenerativeAI(
                    google_api_key=self.api_key,
                    model=self.model or "gemini-pro"
                )
        except Exception as e:
            st.error(f"Error setting up {self.provider} client: {str(e)}")
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using the selected LLM"""
        try:
            if not self.client:
                return "Error: LLM client not properly configured"
            
            prompt = f"""Context: {context}

Question: {query}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information to answer the question, please say so."""
            
            if self.provider == "Azure":
                # Use Azure OpenAI client directly
                response = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant  that answers questions based on the provided document context.",
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    max_tokens=4096,
                    temperature=0.7,
                    top_p=1.0,
                    model=self.model or "gpt-4o"
                )
                return response.choices[0].message.content
            else:
                # Use LangChain for other providers
                response = self.client.invoke(prompt)
                return response.content
                
        except Exception as e:
            return f"Error generating response: {str(e)}"

def remove_document(filename: str):
    """Remove a document from the system"""
    if st.session_state.vector_db:
        if st.session_state.vector_db.remove_document(filename):
            # Remove from session state
            st.session_state.uploaded_pdfs = [
                pdf for pdf in st.session_state.uploaded_pdfs 
                if pdf['filename'] != filename
            ]
            st.success(f"✅ Removed {filename} from the system")
            st.rerun()
        else:
            st.error(f"❌ Failed to remove {filename}")

def main():
    # Header with modern design
    st.markdown('<h1 class="main-header">📚 PDF Knowledge Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("""
        <div class="modern-card">
            <h3>⚙️ Configuration</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Model Selection
        st.subheader("🤖 LLM Provider")
        provider = st.selectbox(
            "Choose your LLM provider:",
            ["OpenAI", "Claude", "Azure", "Grok"],
            help="Select the AI model provider you want to use"
        )
        
        # API Key input
        api_key = st.text_input(
            "API Key:",
            type="password",
            help=f"Enter your {provider} API key"
        )
        
        # Azure-specific configuration
        azure_endpoint = None
        if provider == "Azure":
            azure_endpoint = st.text_input(
                "Azure Endpoint:",
                value="https://ramishjamal18-1741-resource.cognitiveservices.azure.com/",
                help="Your Azure OpenAI endpoint URL"
            )
        
        # Model selection based on provider
        if provider == "OpenAI":
            model = st.selectbox(
                "Model:",
                ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
                help="Select the OpenAI model to use"
            )
        elif provider == "Claude":
            model = st.selectbox(
                "Model:",
                ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"],
                help="Select the Claude model to use"
            )
        elif provider == "Azure":
            model = st.selectbox(
                "Model:",
                ["gpt-4o", "gpt-35-turbo", "gpt-4", "gpt-4-32k"],
                help="Select the Azure OpenAI model to use"
            )
        elif provider == "Grok":
            model = st.selectbox(
                "Model:",
                ["gemini-pro", "gemini-pro-vision"],
                help="Select the Google Gemini model to use"
            )
        
        # Vector database settings
        st.markdown("""
        <div class="modern-card">
            <h4>🗄️ Vector Database</h4>
        </div>
        """, unsafe_allow_html=True)
        
        collection_name = st.text_input(
            "Collection Name:",
            value="pdf_knowledge_base",
            help="Name for the vector database collection"
        )
        
        chunk_size = st.slider(
            "Chunk Size:",
            min_value=500,
            max_value=2000,
            value=1000,
            step=100,
            help="Size of text chunks for processing"
        )
        
        overlap = st.slider(
            "Chunk Overlap:",
            min_value=0,
            max_value=500,
            value=200,
            step=50,
            help="Overlap between consecutive chunks"
        )
        
        # Status indicator
        if st.session_state.vector_db:
            st.markdown("""
            <div style="display: flex; align-items: center; margin: 1rem 0;">
                <span class="status-indicator status-active"></span>
                <span>Vector DB Active</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h3>📄 PDF Upload & Processing</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # File upload with modern styling
        uploaded_files = st.file_uploader(
            "Upload PDF files:",
            type=['pdf'],
            accept_multiple_files=True,
            help="Select one or more PDF files to process"
        )
        
        if uploaded_files and st.button("🚀 Process PDFs", type="primary"):
            if not api_key:
                st.error("Please enter an API key first!")
            elif provider == "Azure" and not azure_endpoint:
                st.error("Please enter your Azure endpoint for Azure OpenAI!")
            else:
                with st.spinner("Processing PDFs..."):
                    # Initialize components
                    processor = PDFProcessor()
                    vector_db = VectorDatabase()
                    
                    # Create collection
                    vector_db.create_collection(collection_name)
                    st.session_state.current_collection = collection_name
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    total_chunks = 0
                    for i, pdf_file in enumerate(uploaded_files):
                        status_text.text(f"Processing {pdf_file.name}...")
                        progress_bar.progress((i + 1) / len(uploaded_files))
                        
                        # Extract text
                        text = processor.extract_text_from_pdf(pdf_file)
                        if text:
                            # Chunk text
                            chunks = processor.chunk_text(text, chunk_size, overlap)
                            
                            # Create embeddings
                            embeddings = processor.create_embeddings(chunks)
                            
                            # Prepare metadata
                            metadata = [
                                {
                                    "filename": pdf_file.name,
                                    "chunk_index": j,
                                    "total_chunks": len(chunks),
                                    "upload_time": datetime.now().isoformat(),
                                    "document_id": str(uuid.uuid4())
                                }
                                for j in range(len(chunks))
                            ]
                            
                            # Add to vector database
                            vector_db.add_documents(chunks, embeddings, metadata)
                            total_chunks += len(chunks)
                            
                            # Store in session state
                            st.session_state.uploaded_pdfs.append({
                                "filename": pdf_file.name,
                                "chunks": len(chunks),
                                "text": text[:500] + "..." if len(text) > 500 else text,
                                "upload_time": datetime.now().isoformat(),
                                "document_id": metadata[0]["document_id"]
                            })
                    
                    st.session_state.vector_db = vector_db
                    st.session_state.embeddings_model = processor.embeddings_model
                    
                    progress_bar.progress(1.0)
                    status_text.text("✅ Processing complete!")
                    
                    st.success(f"✅ Processed {len(uploaded_files)} PDF(s) with {total_chunks} total chunks!")
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
        
        # Display uploaded PDFs with management options
        if st.session_state.uploaded_pdfs:
            st.markdown("""
            <div class="modern-card">
                <h4>📚 Processed Documents</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for pdf in st.session_state.uploaded_pdfs:
                # Create a modern document card
                with st.container():
                    st.markdown(f"""
                    <div class="modern-card" style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                            <div>
                                <h4 style="margin: 0; color: var(--primary-color);">📄 {pdf['filename']}</h4>
                                <p style="margin: 0.5rem 0; color: var(--text-secondary);">
                                    <strong>Chunks:</strong> {pdf['chunks']} | 
                                    <strong>Uploaded:</strong> {pdf['upload_time'][:19]}
                                </p>
                            </div>
                            <div style="display: flex; gap: 0.5rem;">
                                <button class="action-btn" style="background: var(--error-color); color: white; border: none; padding: 0.5rem; border-radius: 8px; cursor: pointer;" 
                                        onclick="this.closest('.modern-card').style.display='none'">🗑️</button>
                            </div>
                        </div>
                        
                        <details style="margin-top: 1rem;">
                            <summary style="cursor: pointer; color: var(--primary-color); font-weight: 600;">📖 Preview Content</summary>
                                                    <div style="background: var(--bg-tertiary); padding: 1rem; border-radius: 8px; margin-top: 0.5rem; max-height: 200px; overflow-y: auto; color: var(--text-primary);">
                            {pdf['text']}
                        </div>
                        </details>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add Streamlit remove button below the card
                col_view, col_remove = st.columns([3, 1])
                with col_view:
                    if st.button(f"👁️ View Details", key=f"view_{pdf['filename']}", type="secondary"):
                        st.info(f"Document: {pdf['filename']}\nChunks: {pdf['chunks']}\nUpload Time: {pdf['upload_time'][:19]}")
                
                with col_remove:
                    if st.button(f"🗑️ Remove", key=f"remove_{pdf['filename']}", type="secondary"):
                        remove_document(pdf['filename'])
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <h3>💬 Chat Interface</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced chat input
        chat_input_container = st.container()
        with chat_input_container:
            col_input, col_send = st.columns([4, 1])
            
            with col_input:
                user_query = st.text_input(
                    "Ask a question about your PDFs:",
                    placeholder="e.g., What are the main topics discussed in the documents?",
                    help="Ask questions about the content of your uploaded PDFs",
                    key="chat_input"
                )
            
            with col_send:
                send_button = st.button("🔍", help="Send question", key="send_button")
        
        # Process chat
        if (user_query and send_button) or (user_query and st.session_state.get('auto_send', False)):
            if not st.session_state.vector_db or not st.session_state.embeddings_model:
                st.error("Please upload and process PDFs first!")
            elif not api_key:
                st.error("Please enter an API key first!")
            elif provider == "Azure" and not azure_endpoint:
                st.error("Please enter your Azure endpoint for Azure OpenAI!")
            else:
                with st.spinner("Searching and generating answer..."):
                    # Search for relevant context
                    search_results = st.session_state.vector_db.search_similar(
                        user_query, 
                        st.session_state.embeddings_model
                    )
                    
                    if search_results and search_results['documents']:
                        # Combine relevant context
                        context = "\n\n".join(search_results['documents'][0])
                        
                        # Initialize LLM provider
                        llm = LLMProvider(provider, api_key, model, azure_endpoint)
                        
                        # Generate response
                        response = llm.generate_response(user_query, context)
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "user": user_query,
                            "assistant": response,
                            "timestamp": datetime.now().strftime("%H:%M"),
                            "context_sources": [search_results['metadatas'][0][i].get('filename', 'Unknown') for i in range(len(search_results['metadatas'][0]))]
                        })
                        
                        # Clear input by rerunning to reset the form
                        st.rerun()
                    else:
                        st.warning("No relevant context found in the documents.")
        
        # Enhanced chat history display
        if st.session_state.chat_history:
            st.markdown("""
            <div class="chat-container">
                <h4>💭 Chat History</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for i, message in enumerate(reversed(st.session_state.chat_history)):
                # User message
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You</strong>
                    <div style="margin: 0.5rem 0;">{message['user']}</div>
                    <span class="message-timestamp">{message['timestamp']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Assistant message with context sources
                context_sources = message.get('context_sources', [])
                sources_text = ""
                if context_sources:
                    unique_sources = list(set(context_sources))
                    sources_text = f"<div style='font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.5rem;'><strong>Sources:</strong> {', '.join(unique_sources)}</div>"
                
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant</strong>
                    <div style="margin: 0.5rem 0;">{message['assistant']}</div>
                    {sources_text}
                    <span class="message-timestamp">{message['timestamp']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat management
        if st.session_state.chat_history:
            col_clear, col_export = st.columns([1, 1])
            
            with col_clear:
                if st.button("🗑️ Clear Chat", type="secondary"):
                    st.session_state.chat_history = []
                    st.rerun()
            
            with col_export:
                if st.button("📤 Export Chat", type="secondary"):
                    # Export chat history
                    chat_data = {
                        "export_time": datetime.now().isoformat(),
                        "total_messages": len(st.session_state.chat_history),
                        "messages": st.session_state.chat_history
                    }
                    
                    # Create download button
                    st.download_button(
                        label="Download Chat History",
                        data=json.dumps(chat_data, indent=2),
                        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
    
    # Footer with modern design
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: var(--text-secondary); padding: 2rem 0;'>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>Built with ❤️ using Streamlit, LangChain, and ChromaDB</p>
        <p style='font-size: 0.9rem;'>Support for OpenAI, Claude, Azure OpenAI, and Google Gemini</p>
        <div style='margin-top: 1rem;'>
            <span style='background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 600;'>PDF Knowledge Assistant v2.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
