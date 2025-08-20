@echo off
chcp 65001 >nul
echo 🚀 Starting PDF Knowledge Assistant...
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
python -c "import streamlit, chromadb, sentence_transformers" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing requirements...
    pip install -r requirements.txt
    echo ✅ Requirements installed
) else (
    echo ✅ Requirements already installed
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating template...
    (
        echo # PDF Knowledge Assistant Environment Variables
        echo # Add your API keys below
        echo.
        echo # OpenAI Configuration
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo.
        echo # Anthropic ^(Claude^) Configuration
        echo ANTHROPIC_API_KEY=your_anthropic_api_key_here
        echo.
        echo # Azure OpenAI Configuration
        echo AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
        echo AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
        echo.
        echo # Google Generative AI ^(Gemini^) Configuration
        echo GOOGLE_API_KEY=your_google_api_key_here
        echo.
        echo # Vector Database Configuration
        echo CHROMA_DB_PATH=./chroma_db
    ) > .env
    echo ✅ .env template created
    echo ⚠️  Please edit .env file with your actual API keys before continuing
    echo Press any key to continue or close this window to edit .env file...
    pause >nul
)

REM Create necessary directories
if not exist "chroma_db" mkdir chroma_db
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs

echo 🚀 Starting the application...
echo 📱 The app will open in your browser at http://localhost:8501
echo 🛑 Press Ctrl+C to stop the application
echo ======================================

REM Start the Streamlit application
streamlit run app.py

pause
