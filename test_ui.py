import streamlit as st

# Page configuration
st.set_page_config(
    page_title="UI Test",
    page_icon="🧪",
    layout="wide"
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
</style>
""", unsafe_allow_html=True)

# Test the modern CSS
st.markdown("""
<style>
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .test-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
    }
    
    .test-card {
        background: #1f2937;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border: 1px solid #4b5563;
        transition: all 0.3s ease;
        color: #f9fafb;
    }
    
    .test-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("🧪 UI Test - Modern Elements")

# Test gradient header
st.markdown('<h1 class="test-header">🎨 Gradient Header Test</h1>', unsafe_allow_html=True)

# Test modern cards
st.markdown("""
<div class="test-card">
    <h3>✨ Modern Card Test</h3>
    <p>This card should have rounded corners, shadows, and hover effects.</p>
</div>
""", unsafe_allow_html=True)

# Test buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.button("🚀 Primary Button", type="primary")

with col2:
    st.button("⚙️ Secondary Button", type="secondary")

with col3:
    st.button("❌ Danger Button")

# Test file uploader
st.subheader("📁 File Upload Test")
uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf'])

# Test chat interface
st.subheader("💬 Chat Interface Test")
user_input = st.text_input("Ask a question:", placeholder="Type your question here...")
if st.button("Send"):
    if user_input:
        st.success(f"✅ Question received: {user_input}")
    else:
        st.error("❌ Please enter a question")

# Test progress
st.subheader("📊 Progress Test")
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)

st.success("✅ UI Test Complete! All elements should be working.")
