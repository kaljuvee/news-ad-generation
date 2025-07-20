# News-Responsive Ad Generation - Streamlit App

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download NLTK Data (Required for RAG Processing)
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### 3. Set up OpenAI API Key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Run the Streamlit App
```bash
# Option 1: Using the runner script
python run_app.py

# Option 2: Direct streamlit command
streamlit run Home.py
```

### 5. Open in Browser
Navigate to: http://localhost:8501

## 🚀 Streamlit Cloud Deployment

### Automatic Deployment
1. **Push to GitHub**: Upload your code to a GitHub repository
2. **Connect to Streamlit Cloud**: 
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Deploy automatically
3. **No Manual Setup**: NLTK data downloads automatically on first run

### Environment Variables
Set these in Streamlit Cloud:
- `OPENAI_API_KEY`: Your OpenAI API key

### Deployment Notes
- ✅ NLTK data downloads automatically
- ✅ All dependencies handled by requirements.txt
- ✅ No command line setup required
- ✅ Works out of the box on Streamlit Cloud

## 📁 Project Structure

```
news-ad-generation/
├── Home.py                              # 🏠 Main Streamlit app (overview)
├── run_app.py                           # 🚀 App runner script
├── requirements.txt                     # 📦 Dependencies
├── README_STREAMLIT.md                  # 📖 This file
├── utils/                               # 🔧 Core logic (moved from root)
│   ├── parse_client_data.py            # 📊 Excel data parser
│   ├── web_scraper.py                  # 🕷️ Landing page scraper
│   ├── rag_processor.py                # 🧠 Vector database & semantic search
│   ├── openai_ad_generator.py          # 🤖 AI text generation
│   ├── professional_ad_generator.py    # 🎨 Visual ad creation
│   └── main_pipeline.py                # 🔄 Complete pipeline
├── pages/                               # 📄 Streamlit pages
│   ├── 1_📊_Parse_Client_Data.py       # Step 1: Parse Excel data
│   ├── 2_🕷️_Web_Scraper.py            # Step 2: Scrape landing pages
│   ├── 3_🧠_RAG_Processor.py           # Step 3: Build vector database
│   ├── 4_🤖_OpenAI_Ad_Generator.py     # Step 4: Generate AI text campaigns
│   └── 5_🎨_Professional_Ad_Generator.py # Step 5: Create visual ads
├── data/                                # 📂 Data storage
│   ├── parsed_client_data.json         # Parsed Excel data
│   ├── client_data_with_content.json   # Data + scraped content
│   └── processed_client_data_rag.json  # RAG-processed data
├── generated_ads_text/                  # 📝 Text campaign outputs
│   └── ad_campaigns.json               # Generated ad content
└── generated_ads_images/                # 🖼️ Visual campaign outputs
    ├── final_ads/                       # Complete marketing materials
    └── *_bg_*.png                      # Background images
```

## 🧭 Navigation Guide

### Home Page (🏠)
- **Overview**: Complete project description and architecture
- **How It Works**: Step-by-step walkthrough with examples
- **Quick Start**: Installation and setup instructions

### Step 1: Parse Client Data (📊)
- **Purpose**: Parse Excel file with client URLs and news articles
- **Input**: Excel file with multiple sheets (one per client)
- **Output**: Structured JSON data
- **Features**: File upload, default file option, data preview

### Step 2: Web Scraper (🕷️)
- **Purpose**: Extract content from client landing pages
- **Input**: Parsed client data with URLs
- **Output**: Enhanced data with landing page content
- **Features**: Batch scraping, individual client option, content preview

### Step 3: RAG Processor (🧠)
- **Purpose**: Build vector database for semantic search
- **Input**: Scraped client data
- **Output**: FAISS vector index + processed data with relevant news
- **Features**: Model selection, semantic search interface, database statistics

### Step 4: OpenAI Ad Generator (🤖)
- **Purpose**: Generate AI text campaigns using GPT-4o
- **Input**: RAG-processed data
- **Output**: Structured ad campaigns (LinkedIn, banner, additional)
- **Features**: API key management, client selection, campaign preview

### Step 5: Professional Ad Generator (🎨)
- **Purpose**: Create complete visual ads with DALL-E 3
- **Input**: Generated text campaigns
- **Output**: Marketing-ready PNG images with text overlays
- **Features**: Image quality settings, format selection, download options

## 🔧 Usage Instructions

### Command Line vs Streamlit
The project supports both command line and Streamlit interfaces:

**Command Line (Original):**
```bash
cd utils
python parse_client_data.py
python web_scraper.py
python rag_processor.py
python openai_ad_generator.py
python professional_ad_generator.py
```

**Streamlit (New):**
```bash
streamlit run Home.py
# Then use the web interface to navigate through steps
```

### Data Flow
1. **Excel File** → Parse Client Data → `data/parsed_client_data.json`
2. **Parsed Data** → Web Scraper → `data/client_data_with_content.json`
3. **Scraped Data** → RAG Processor → `data/processed_client_data_rag.json`
4. **RAG Data** → OpenAI Generator → `generated_ads_text/ad_campaigns.json`
5. **Text Campaigns** → Professional Generator → `generated_ads_images/final_ads/`

### Session State
The Streamlit app uses session state to maintain data between pages:
- `st.session_state.parsed_data`: Parsed client data
- `st.session_state.client_data_with_content`: Scraped data
- `st.session_state.processed_data`: RAG-processed data
- `st.session_state.generated_campaigns`: Generated text campaigns
- `st.session_state.rag_processor`: RAG processor instance

## 🎯 Key Features

### ✅ No Code Duplication
- Core logic remains in `utils/` directory
- Streamlit pages import and reuse existing functions
- Single source of truth for all functionality

### ✅ Dual Interface Support
- Run from command line for automation
- Use Streamlit for interactive development
- Same underlying code, different interfaces

### ✅ Interactive Dashboard
- Real-time progress tracking
- Data preview and validation
- Error handling and status updates
- Download capabilities

### ✅ Flexible Configuration
- API key management
- Model selection
- Parameter tuning
- Client selection

## 🚨 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure utils directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/utils"
```

**2. Missing Dependencies**
```bash
# Install all requirements
pip install -r requirements.txt
```

**3. NLTK Data Issues (RAG Processor)**
```bash
# Download required NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# If you get permission errors, try:
python -c "import nltk; nltk.download('stopwords', download_dir='./nltk_data'); nltk.download('punkt', download_dir='./nltk_data')"
```

**4. OpenAI API Issues**
```bash
# Check API key in .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

**5. File Permission Issues**
```bash
# Make runner script executable
chmod +x run_app.py
```

### Debug Mode
Run with debug information:
```bash
streamlit run Home.py --logger.level debug
```

## 📊 Performance Tips

1. **Use Default Files**: Start with provided Excel file for testing
2. **Selective Processing**: Choose specific clients to reduce processing time
3. **Batch Operations**: Use batch processing for multiple clients
4. **Cache Results**: Reuse existing data files when available

## 🔄 Pipeline Automation

For automated runs, you can still use the original command line interface:

```bash
# Run complete pipeline
cd utils
python main_pipeline.py

# Or run individual steps
python parse_client_data.py
python web_scraper.py
python rag_processor.py
python openai_ad_generator.py
python professional_ad_generator.py
```

## 📈 Next Steps

1. **Customization**: Modify prompts and parameters in `utils/` files
2. **Integration**: Connect to external data sources
3. **Scaling**: Add support for more clients and formats
4. **Deployment**: Deploy Streamlit app to cloud platforms

---

**Happy Ad Generation! 🚀** 