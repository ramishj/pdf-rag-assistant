#!/usr/bin/env python3
"""
Demo script for PDF Knowledge Assistant
Shows how to use the core functionality programmatically
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from app import PDFProcessor, VectorDatabase, LLMProvider

def demo_pdf_processing():
    """Demonstrate PDF processing capabilities"""
    print("📄 PDF Processing Demo")
    print("=" * 40)
    
    # Initialize processor
    processor = PDFProcessor()
    print("✅ PDF Processor initialized")
    
    # Sample text for demonstration
    sample_text = """
    This is a sample document about artificial intelligence and machine learning.
    AI has revolutionized many industries including healthcare, finance, and transportation.
    Machine learning algorithms can now process vast amounts of data to identify patterns.
    Deep learning has enabled breakthroughs in computer vision and natural language processing.
    The future of AI holds great promise for solving complex problems.
    """
    
    # Process text
    chunks = processor.chunk_text(sample_text, chunk_size=100, overlap=20)
    print(f"✅ Text chunked into {len(chunks)} segments")
    
    # Create embeddings
    embeddings = processor.create_embeddings(chunks)
    print(f"✅ Created {len(embeddings)} embeddings")
    
    return processor, chunks, embeddings

def demo_vector_database(chunks, embeddings):
    """Demonstrate vector database operations"""
    print("\n🗄️ Vector Database Demo")
    print("=" * 40)
    
    # Initialize database
    vector_db = VectorDatabase()
    collection_name = "demo_collection"
    
    # Create collection
    vector_db.create_collection(collection_name)
    print(f"✅ Created collection: {collection_name}")
    
    # Add documents
    metadata = [
        {
            "filename": "demo_doc.txt",
            "chunk_index": i,
            "total_chunks": len(chunks),
            "demo": True
        }
        for i in range(len(chunks))
    ]
    
    vector_db.add_documents(chunks, embeddings, metadata)
    print(f"✅ Added {len(chunks)} documents to database")
    
    return vector_db

def demo_search_and_query(vector_db, processor):
    """Demonstrate search and query capabilities"""
    print("\n🔍 Search and Query Demo")
    print("=" * 40)
    
    # Test queries
    test_queries = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "What are the applications of AI?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        
        # Search for similar documents
        results = vector_db.search_similar(query, processor.embeddings_model, n_results=2)
        
        if results and results['documents']:
            print("Relevant context found:")
            for i, doc in enumerate(results['documents'][0]):
                print(f"  {i+1}. {doc[:100]}...")
        else:
            print("No relevant context found")
    
    return test_queries

def demo_llm_providers():
    """Demonstrate LLM provider setup"""
    print("\n🤖 LLM Provider Demo")
    print("=" * 40)
    
    providers = ["OpenAI", "Claude", "Azure", "Grok"]
    
    for provider in providers:
        print(f"\nProvider: {provider}")
        
        # Get API key from environment
        api_key = os.getenv(f"{provider.upper()}_API_KEY")
        
        if api_key and api_key != "your_api_key_here":
            print(f"✅ API key found for {provider}")
            
            # For Azure, also check endpoint
            azure_endpoint = None
            if provider == "Azure":
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
                if azure_endpoint:
                    print(f"✅ Azure endpoint found: {azure_endpoint}")
                else:
                    print("⚠️  No Azure endpoint found")
                    continue
            
            # Try to initialize provider
            try:
                llm = LLMProvider(provider, api_key, azure_endpoint=azure_endpoint)
                if llm.client:
                    print(f"✅ {provider} client initialized successfully")
                    
                    # Test Azure-specific functionality
                    if provider == "Azure":
                        print(f"   Using endpoint: {azure_endpoint}")
                        print(f"   Default model: gpt-4o")
                else:
                    print(f"⚠️  {provider} client initialization failed")
            except Exception as e:
                print(f"❌ Error initializing {provider}: {str(e)}")
        else:
            print(f"⚠️  No API key found for {provider}")
            if provider == "Azure":
                print(f"   Set {provider.upper()}_API_KEY and AZURE_OPENAI_ENDPOINT in your .env file")
            else:
                print(f"   Set {provider.upper()}_API_KEY in your .env file")

def demo_azure_integration():
    """Demonstrate Azure OpenAI integration specifically"""
    print("\n🔵 Azure OpenAI Integration Demo")
    print("=" * 40)
    
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    if api_key and endpoint and api_key != "your_api_key_here":
        print("✅ Azure credentials found")
        print(f"   Endpoint: {endpoint}")
        
        try:
            # Test Azure client initialization
            llm = LLMProvider("Azure", api_key, "gpt-4o", endpoint)
            if llm.client:
                print("✅ Azure OpenAI client initialized successfully")
                
                # Test a simple query
                test_response = llm.generate_response(
                    "What is the capital of France?", 
                    "France is a country in Europe."
                )
                print(f"✅ Test query successful: {test_response[:100]}...")
            else:
                print("❌ Azure client initialization failed")
        except Exception as e:
            print(f"❌ Azure integration error: {str(e)}")
    else:
        print("⚠️  Azure credentials not found")
        print("   Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in your .env file")

def main():
    """Run the complete demo"""
    print("🚀 PDF Knowledge Assistant Demo")
    print("=" * 50)
    
    try:
        # Demo 1: PDF Processing
        processor, chunks, embeddings = demo_pdf_processing()
        
        # Demo 2: Vector Database
        vector_db = demo_vector_database(chunks, embeddings)
        
        # Demo 3: Search and Query
        test_queries = demo_search_and_query(vector_db, processor)
        
        # Demo 4: LLM Providers
        demo_llm_providers()
        
        # Demo 5: Azure Integration
        demo_azure_integration()
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\n📋 What we demonstrated:")
        print("• PDF text processing and chunking")
        print("• Vector database operations")
        print("• Similarity search functionality")
        print("• LLM provider configuration")
        print("• Azure OpenAI direct integration")
        print("\n🚀 Ready to run the full application!")
        print("Run: python3 run.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        print("Please check your setup and try again")

if __name__ == "__main__":
    main()
