import streamlit as st
import sys
import os
import json
from pathlib import Path

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

# Import the existing parsing logic
from parse_client_data import parse_client_data

# Page configuration
st.set_page_config(
    page_title="Parse Client Data",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Parse Client Data")
st.markdown("Parse Excel file containing client URLs and related news articles")

# File upload section
st.header("📁 Input Data")
st.markdown("Upload the Excel file with client URLs and news articles:")

uploaded_file = st.file_uploader(
    "Choose Excel file", 
    type=['xlsx', 'xls'],
    help="Upload the Excel file containing client URLs and news articles"
)

# Default file option
use_default = st.checkbox("Use default file (URL_and_news_articles_examples_by_client.xlsx)", value=True)

# Process button
if st.button("🚀 Parse Client Data", type="primary"):
    if uploaded_file is not None or use_default:
        with st.spinner("Parsing client data..."):
            try:
                # Determine file path
                if uploaded_file is not None:
                    # Save uploaded file temporarily
                    temp_path = "temp_upload.xlsx"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    file_path = temp_path
                else:
                    file_path = "URL_and_news_articles_examples_by_client.xlsx"
                
                # Parse the data using existing logic
                parsed_data = parse_client_data(file_path)
                
                # Save to data directory
                data_dir = Path("data")
                data_dir.mkdir(exist_ok=True)
                
                output_path = data_dir / "parsed_client_data.json"
                with open(output_path, 'w') as f:
                    json.dump(parsed_data, f, indent=4)
                
                # Clean up temp file if used
                if uploaded_file is not None and os.path.exists(temp_path):
                    os.remove(temp_path)
                
                st.success(f"✅ Successfully parsed {len(parsed_data)} clients!")
                st.markdown(f"**Output saved to:** `{output_path}`")
                
                # Display results
                st.header("📋 Parsed Data Summary")
                
                for i, client in enumerate(parsed_data):
                    with st.expander(f"🏢 {client['client_name']}", expanded=(i==0)):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**URL:** {client['url']}")
                            st.markdown(f"**News Articles:** {len(client['news_articles'])}")
                        
                        with col2:
                            st.markdown("**Sample News Articles:**")
                            for j, article in enumerate(client['news_articles'][:3]):
                                st.markdown(f"{j+1}. {article['title'][:80]}...")
                            
                            if len(client['news_articles']) > 3:
                                st.markdown(f"... and {len(client['news_articles']) - 3} more")
                
                # Store in session state for other pages
                st.session_state.parsed_data = parsed_data
                st.session_state.parsed_data_path = str(output_path)
                
            except Exception as e:
                st.error(f"❌ Error parsing data: {str(e)}")
                st.exception(e)
    else:
        st.warning("⚠️ Please upload a file or use the default file option.")

# Display existing data if available
if os.path.exists("data/parsed_client_data.json"):
    st.header("📂 Existing Data")
    st.markdown("Found existing parsed data:")
    
    try:
        with open("data/parsed_client_data.json", 'r') as f:
            existing_data = json.load(f)
        
        st.success(f"✅ Found {len(existing_data)} clients in existing data")
        
        # Load into session state
        st.session_state.parsed_data = existing_data
        st.session_state.parsed_data_path = "data/parsed_client_data.json"
        
        # Show preview
        with st.expander("👀 Preview Existing Data"):
            for client in existing_data[:2]:  # Show first 2 clients
                st.markdown(f"**{client['client_name']}** - {len(client['news_articles'])} articles")
        
    except Exception as e:
        st.error(f"❌ Error loading existing data: {str(e)}")

# Instructions
with st.expander("ℹ️ Instructions"):
    st.markdown("""
    **This step parses the Excel file containing:**
    - Client URLs for landing pages
    - Related news articles for each client
    - Metadata (titles, sources, dates)
    
    **Expected Excel format:**
    - Multiple sheets (one per client)
    - URL row starting with "URL -"
    - News articles with columns: Title, Source, Published Date, URL
    
    **Output:**
    - Structured JSON data saved to `data/parsed_client_data.json`
    - Data available for next pipeline steps
    """)

# Next steps
st.header("➡️ Next Steps")
st.markdown("""
After parsing the client data, proceed to:
1. **🕷️ Web Scraper** - Extract content from client landing pages
2. **🧠 RAG Processor** - Build vector database for semantic search
3. **🤖 OpenAI Ad Generator** - Generate AI text campaigns
4. **🎨 Professional Ad Generator** - Create visual ads
""") 