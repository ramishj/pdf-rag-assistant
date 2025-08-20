#!/bin/bash

# PDF Knowledge Assistant Startup Script
# This script helps you start the application with proper setup

echo "🚀 Starting PDF Knowledge Assistant..."
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python3 -c "import streamlit, chromadb, sentence_transformers" &> /dev/null; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
    echo "✅ Requirements installed"
else
    echo "✅ Requirements already installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# PDF Knowledge Assistant Environment Variables
# Add your API keys below

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Claude) Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://ramishjamal18-1741-resource.cognitiveservices.azure.com/

# Google Generative AI (Gemini) Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Vector Database Configuration
CHROMA_DB_PATH=./chroma_db
EOF
    echo "✅ .env template created"
    echo "⚠️  Please edit .env file with your actual API keys before continuing"
    echo "Press Enter to continue or Ctrl+C to exit and edit .env file..."
    read
fi

# Create necessary directories
mkdir -p chroma_db uploads logs

echo "🚀 Starting the application..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo "======================================"

# Start the Streamlit application using the virtual environment's streamlit
venv/bin/streamlit run app.py
