import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="News-Responsive Ad Generation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .feature-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .code-block {
        background-color: #f1f2f6;
        padding: 1rem;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📊 News-Responsive Ad Generation with RAG Architecture</h1>', unsafe_allow_html=True)

# Project Goal
st.markdown('<h2 class="section-header">🎯 Project Goal</h2>', unsafe_allow_html=True)
st.markdown("""
This project addresses a critical challenge in asset management marketing: **manually creating timely, relevant ad content that connects client investment insights with the rapidly evolving news cycle**. 

Our solution is an **AI-powered, RAG-enabled system** that automatically generates context-aware ad creative by:
- Analyzing client landing pages to understand their investment expertise and value proposition
- Using semantic search to find relevant financial news from current market developments  
- Generating professional, compliant ad copy that meaningfully connects client strengths with news themes
- Creating complete marketing materials with AI-generated images and text overlays
- Supporting multiple digital ad formats (LinkedIn, banner ads, etc.)
""")

# Key Features
st.markdown('<h2 class="section-header">🚀 Key Features</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - **Real OpenAI GPT-4o Integration**: Production-ready AI ad generation using latest models
    - **RAG (Retrieval-Augmented Generation)**: Vector database with semantic search for precise news relevance
    - **Professional Image Generation**: DALL-E 3 HD integration with text overlays
    - **Multi-Client Support**: Processes multiple asset management firms simultaneously
    """)

with col2:
    st.markdown("""
    - **Compliance-Aware**: Maintains professional, regulatory-compliant tone for financial services
    - **Complete Marketing Pipeline**: End-to-end automated workflow from data to deployment-ready ads
    - **Scalable Architecture**: Modular design supporting easy expansion and customization
    - **Interactive Dashboard**: Streamlit-based interface for easy monitoring and control
    """)

# How It Works
st.markdown('<h2 class="section-header">🚀 How It Works: Step-by-Step Example</h2>', unsafe_allow_html=True)
st.markdown("Let's walk through exactly how the system transforms raw data into professional ad campaigns using **PIMCO** as our example:")

# Step 1: Data Input
with st.expander("📊 Step 1: Data Input", expanded=True):
    st.markdown("""
    ```
    Input File: URL_and_news_articles_examples_by_client.xlsx
    - PIMCO URL: https://www.pimco.com/us/en/insights/fed-policymakers-split-decision
    - State Street URL: https://www.ssga.com/uk/en_gb/institutional/capabilities/esg
    - T. Rowe Price URL: https://www.troweprice.com/en/institutional/capabilities
    - 265+ financial news articles embedded in vector database
    ```
    """)

# Step 2: Web Scraping
with st.expander("🕷️ Step 2: Web Scraping", expanded=True):
    st.markdown("""
    ```python
    # System scrapes PIMCO's landing page
    Scraped Content (sample):
    "SPDR® Gold MiniShares® Trust, sustainable investing screening, 
    ESG capabilities, environmental social governance solutions, 
    institutional investment strategies..."

    Result: 20,156 characters of landing page content
    ```
    """)

# Step 3: RAG Processing
with st.expander("🧠 Step 3: RAG Processing & Vector Database", expanded=True):
    st.markdown("""
    ```python
    # System builds FAISS vector database with 265 embeddings
    Vector Database: 384-dimensional embeddings using Sentence-BERT
    Embedding Model: "all-MiniLM-L6-v2"

    # For PIMCO (Fed policy focus):
    Query: "Fed policymakers split decision + location americas + asia pacific"
    Semantic Search Results:
    ✅ "Emerging markets gains in the cards as Trump's tariffs..." → Score: 0.31
    ✅ "Fed Forced to Balance Policy Predicament..." → Score: 0.39
    ❌ "Sustainable investing trends" → Score: 0.12 (not relevant)
    ```
    """)

# Step 4: AI Generation
with st.expander("🤖 Step 4: AI Ad Generation with GPT-4o", expanded=True):
    st.markdown("""
    ```python
    # OpenAI GPT-4o receives structured prompt with RAG context:
    "Client: PIMCO
    Landing Page Content: Fed policymakers split decision analysis...
    Relevant News: 
    1. Emerging markets gains as Trump's tariffs challenge... (Score: 0.31)
    2. Fed Forced to Balance Policy Predicament... (Score: 0.39)

    Task: Generate LinkedIn ad, banner ad, and additional creative
    Format: JSON with headline, body, CTA, image_description
    Tone: Professional, compliant, thought leadership"

    GPT-4o Response: [Contextually relevant ad content with news connections]
    ```
    """)

# Architecture Overview
st.markdown('<h2 class="section-header">🏗️ Architecture Overview</h2>', unsafe_allow_html=True)
st.markdown("""
```
📊 Excel Data → 🕷️ Web Scraping → 🧠 RAG Vector DB → 🤖 GPT-4o → 🎨 DALL-E 3 → 📢 Complete Ads
    ↓               ↓                    ↓              ↓           ↓             ↓
Parsed URLs     Landing Page      FAISS Index     Structured   HD Images    Marketing-Ready
& News Data     Content (20K+)   (265 vectors)   Prompts      + Text       Materials
                                  384-dim                      Overlays
```
""")

# Core Components
st.markdown('<h3>Core Components</h3>', unsafe_allow_html=True)
components = [
    ("Data Ingestion Layer", "parse_client_data.py", "Parses Excel file with client URLs and news articles"),
    ("Web Scraping Layer", "web_scraper.py", "Extracts content from client landing pages"),
    ("RAG Processing Layer", "rag_processor.py", "Builds FAISS vector database with semantic search"),
    ("AI Generation Layer", "openai_ad_generator.py", "Real OpenAI GPT-4o integration with structured prompts"),
    ("Image Generation Layer", "professional_ad_generator.py", "DALL-E 3 HD integration for background images"),
    ("Pipeline Orchestration", "main_pipeline.py", "Automated end-to-end workflow")
]

for component, file, description in components:
    with st.expander(f"🔧 {component} ({file})"):
        st.markdown(f"**{description}**")

# Repository Structure
st.markdown('<h2 class="section-header">📁 Repository Structure</h2>', unsafe_allow_html=True)
st.code("""
news_generation/
├── README.md                           # This file
├── .env                               # OpenAI API key (secure)
├── .gitignore                         # Protects sensitive files
├── main_pipeline.py                   # 🚀 Main execution script
├── parse_client_data.py               # Excel data parser
├── web_scraper.py                     # Landing page scraper  
├── rag_processor.py                   # Vector database & semantic search
├── openai_ad_generator.py             # AI ad generation with GPT-4o
├── professional_ad_generator.py       # DALL-E 3 + text overlay system
├── solution_design.md                 # Technical design document
├── data/                              # Organized data folder
│   ├── parsed_client_data.json       # Parsed Excel data
│   ├── client_data_with_content.json # Data + scraped content
│   └── processed_client_data_rag.json # RAG-processed data
├── generated_ads_text/                # Text campaign outputs
│   └── ad_campaigns.json             # Structured ad content
└── generated_ads_images/              # Visual campaign outputs
    ├── final_ads/                     # Complete marketing materials
    └── *_bg_*.png                    # Background images
""")

# Quick Start
st.markdown('<h2 class="section-header">⚡ Quick Start</h2>', unsafe_allow_html=True)
st.markdown("""
### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Download required NLTK data (for RAG processing)
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Add your OpenAI API key to .env file
# Edit .env and replace 'your-openai-api-key-here' with your actual key
```

### ⚠️ Important: NLTK Data Setup
The RAG processor requires NLTK data for keyword extraction. If you encounter NLTK errors, run:
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### 🚀 Streamlit Cloud Deployment
For deployment on Streamlit Cloud:
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. The app will automatically download NLTK data on first run
4. No manual setup required - everything is handled automatically
""")

# Navigation Instructions
st.markdown('<h2 class="section-header">🧭 Navigation</h2>', unsafe_allow_html=True)
st.markdown("""
Use the sidebar to navigate through the different pipeline components:

1. **📊 Parse Client Data** - Parse Excel data and extract client information
2. **🕷️ Web Scraper** - Scrape landing pages for content analysis
3. **🧠 RAG Processor** - Build vector database and perform semantic search
4. **🤖 OpenAI Ad Generator** - Generate AI text campaigns with GPT-4o
5. **🎨 Professional Ad Generator** - Create complete visual ads with DALL-E 3

Each page provides an interactive interface to run the respective pipeline component and view results.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>News-Responsive Ad Generation System | Built with Streamlit & OpenAI</p>
</div>
""", unsafe_allow_html=True) 