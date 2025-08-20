#!/usr/bin/env python3
"""
Setup script for PDF Knowledge Assistant
Automatically installs dependencies and creates necessary directories
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file with template"""
    env_file = Path(".env")
    if env_file.exists():
        print("ℹ️  .env file already exists")
        return True
    
    env_template = """# PDF Knowledge Assistant Environment Variables
# Add your API keys below

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Claude) Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Google Generative AI (Gemini) Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Vector Database Configuration
CHROMA_DB_PATH=./chroma_db
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_template)
        print("✅ Created .env file template")
        print("⚠️  Please edit .env file with your actual API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["chroma_db", "uploads", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Created necessary directories")
    return True

def run_tests():
    """Run basic tests to ensure everything is working"""
    print("🧪 Running basic tests...")
    try:
        # Test imports
        import streamlit
        import chromadb
        import sentence_transformers
        print("✅ All core packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up PDF Knowledge Assistant...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your API keys")
    print("2. Run: streamlit run app.py")
    print("3. Open http://localhost:8501 in your browser")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
