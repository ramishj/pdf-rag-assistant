#!/usr/bin/env python3
"""
Simple runner script for PDF Knowledge Assistant
This script handles virtual environment activation and runs the app
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def activate_venv():
    """Activate virtual environment if it exists"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
    
    # Get the path to the virtual environment's Python and pip
    if os.name == 'nt':  # Windows
        python_path = venv_path / "Scripts" / "python.exe"
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:  # Unix/Linux/macOS
        python_path = venv_path / "bin" / "python"
        pip_path = venv_path / "bin" / "pip"
    
    return python_path, pip_path

def install_requirements(pip_path):
    """Install required packages"""
    print("📦 Checking requirements...")
    try:
        # Check if key packages are already installed
        result = subprocess.run([
            str(pip_path), "show", "streamlit"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("📦 Installing requirements...")
            subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
            print("✅ Requirements installed")
        else:
            print("✅ Requirements already installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
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
AZURE_OPENAI_ENDPOINT=https://ramishjamal18-1741-resource.cognitiveservices.azure.com/

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

def run_app(python_path):
    """Run the Streamlit application"""
    print("🚀 Starting the application...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("======================================")
    
    try:
        subprocess.run([str(python_path), "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function"""
    print("🚀 PDF Knowledge Assistant Runner")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Activate virtual environment
    python_path, pip_path = activate_venv()
    
    # Install requirements
    if not install_requirements(pip_path):
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Run the application
    run_app(python_path)

if __name__ == "__main__":
    main()
