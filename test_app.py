#!/usr/bin/env python3
"""
Test file for PDF Knowledge Assistant
Runs basic tests to ensure all components are working
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

class TestPDFProcessor(unittest.TestCase):
    """Test PDF processing functionality"""
    
    def setUp(self):
        from app import PDFProcessor
        self.processor = PDFProcessor()
    
    def test_text_chunking(self):
        """Test text chunking functionality"""
        test_text = "This is a test document with multiple sentences. " * 50
        
        chunks = self.processor.chunk_text(test_text, chunk_size=100, overlap=20)
        
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 0)
        
        # Check chunk sizes
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 100)
    
    def test_embeddings_creation(self):
        """Test embedding creation"""
        test_chunks = ["This is a test chunk.", "Another test chunk."]
        
        embeddings = self.processor.create_embeddings(test_chunks)
        
        self.assertIsInstance(embeddings, list)
        self.assertEqual(len(embeddings), len(test_chunks))
        
        # Check embedding dimensions
        for embedding in embeddings:
            self.assertIsInstance(embedding, list)
            self.assertGreater(len(embedding), 0)

class TestVectorDatabase(unittest.TestCase):
    """Test vector database functionality"""
    
    def setUp(self):
        from app import VectorDatabase
        self.vector_db = VectorDatabase()
        self.test_collection = "test_collection"
    
    def test_collection_creation(self):
        """Test collection creation"""
        result = self.vector_db.create_collection(self.test_collection)
        self.assertTrue(result)
    
    def test_document_addition(self):
        """Test adding documents to database"""
        # Create test data
        chunks = ["Test document 1", "Test document 2"]
        embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        metadata = [{"test": True}, {"test": True}]
        
        # Add documents
        self.vector_db.add_documents(chunks, embeddings, metadata)
        
        # This should not raise an exception
        self.assertTrue(True)

class TestLLMProvider(unittest.TestCase):
    """Test LLM provider functionality"""
    
    def test_provider_initialization(self):
        """Test LLM provider initialization"""
        from app import LLMProvider
        
        # Test with invalid provider
        provider = LLMProvider("InvalidProvider", "fake_key")
        self.assertIsNone(provider.client)

class TestConfiguration(unittest.TestCase):
    """Test configuration functionality"""
    
    def test_config_imports(self):
        """Test that configuration can be imported"""
        try:
            import config
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import config: {e}")
    
    def test_llm_providers_config(self):
        """Test LLM providers configuration"""
        import config
        
        providers = ["OpenAI", "Claude", "Azure", "Grok"]
        for provider in providers:
            self.assertIn(provider, config.LLM_PROVIDERS)
            self.assertIn("models", config.LLM_PROVIDERS[provider])
            self.assertIn("default_model", config.LLM_PROVIDERS[provider])

def run_basic_tests():
    """Run basic functionality tests"""
    print("🧪 Running basic tests...")
    
    # Test imports
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError:
        print("❌ Streamlit import failed")
        return False
    
    try:
        import chromadb
        print("✅ ChromaDB imported successfully")
    except ImportError:
        print("❌ ChromaDB import failed")
        return False
    
    try:
        import sentence_transformers
        print("✅ Sentence Transformers imported successfully")
    except ImportError:
        print("❌ Sentence Transformers import failed")
        return False
    
    try:
        import langchain
        print("✅ LangChain imported successfully")
    except ImportError:
        print("❌ LangChain import failed")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Testing PDF Knowledge Assistant...")
    print("=" * 50)
    
    # Run basic import tests
    if not run_basic_tests():
        print("\n❌ Basic tests failed. Please install dependencies first.")
        return
    
    print("\n✅ Basic tests passed!")
    print("\n🧪 Running unit tests...")
    
    # Run unit tests
    try:
        unittest.main(argv=[''], exit=False, verbosity=2)
        print("\n🎉 All tests completed!")
    except Exception as e:
        print(f"\n❌ Unit tests failed: {e}")
    
    print("\n📋 Test Summary:")
    print("• Basic imports: ✅")
    print("• Unit tests: See results above")
    print("\n🚀 Ready to run the application!")

if __name__ == "__main__":
    main()
