# 🚀 Quick Start Guide - PDF Knowledge Assistant

## ⚡ Fastest Way to Run

### Option 1: Python Runner (Recommended)

```bash
python3 run.py
```

### Option 2: Shell Script

```bash
./start.sh
```

### Option 3: Manual Steps

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run the app
streamlit run app.py
```

## 🔑 Setup API Keys

1. **Edit the `.env` file** that was created automatically
2. **Add your API key** for at least one provider:
   - OpenAI: Get key from [OpenAI Platform](https://platform.openai.com/)
   - Claude: Get key from [Anthropic Console](https://console.anthropic.com/)
   - Azure: Get key from Azure Portal
   - Grok: Get key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📱 Access the App

- **URL**: http://localhost:8501
- **Browser**: Opens automatically
- **Stop**: Press `Ctrl+C` in terminal

## 🎯 What to Do Next

1. **Choose LLM Provider** from the sidebar
2. **Enter your API key**
3. **Upload PDF files** (drag & drop)
4. **Process documents** (click "Process PDFs")
5. **Ask questions** in the chat interface

## 🆘 Troubleshooting

- **Port already in use**: Change port with `streamlit run app.py --server.port 8502`
- **Import errors**: Run `python3 run.py` to reinstall dependencies
- **API key issues**: Check your `.env` file and API key validity

## 📚 Sample Document

Use `sample_document.txt` to test the system if you don't have PDFs!

---

**That's it! Your PDF Knowledge Assistant is ready to use! 🎉**
