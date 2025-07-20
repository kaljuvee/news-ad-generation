import streamlit as st
import sys
import os
import json
from pathlib import Path

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

# Import the existing scraping logic
from web_scraper import scrape_text_from_url

# Page configuration
st.set_page_config(
    page_title="Web Scraper",
    page_icon="🕷️",
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
st.title("🕷️ Web Scraper")
st.markdown("Extract content from client landing pages for analysis")

# Check for parsed data
if not os.path.exists("data/parsed_client_data.json"):
    st.error("❌ No parsed client data found. Please run the Parse Client Data step first.")
    st.stop()

# Load parsed data
try:
    with open("data/parsed_client_data.json", 'r') as f:
        client_data = json.load(f)
    st.success(f"✅ Loaded {len(client_data)} clients from parsed data")
except Exception as e:
    st.error(f"❌ Error loading parsed data: {str(e)}")
    st.stop()

# Display clients to be scraped
st.header("📋 Clients to Scrape")
for i, client in enumerate(client_data):
    with st.expander(f"🏢 {client['client_name']}", expanded=(i==0)):
        st.markdown(f"**URL:** {client['url']}")
        st.markdown(f"**News Articles:** {len(client['news_articles'])}")

# Scraping options
st.header("⚙️ Scraping Options")
col1, col2 = st.columns(2)

with col1:
    scrape_all = st.checkbox("Scrape all clients", value=True)
    timeout = st.slider("Timeout (seconds)", 5, 30, 10)

with col2:
    show_content = st.checkbox("Show scraped content preview", value=False)
    save_samples = st.checkbox("Save content samples", value=True)

# Process button
if st.button("🚀 Start Web Scraping", type="primary"):
    if scrape_all or st.session_state.get('selected_client'):
        with st.spinner("Scraping client landing pages..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            successful_scrapes = 0
            failed_scrapes = 0
            
            # Determine which clients to scrape
            clients_to_scrape = client_data if scrape_all else [c for c in client_data if c['client_name'] == st.session_state.get('selected_client')]
            
            for i, client in enumerate(clients_to_scrape):
                status_text.text(f"Scraping {client['client_name']}...")
                
                try:
                    # Scrape the URL using existing logic
                    content = scrape_text_from_url(client['url'])
                    client['landing_page_content'] = content
                    
                    if content:
                        successful_scrapes += 1
                        st.success(f"✅ {client['client_name']}: {len(content)} characters scraped")
                        
                        # Save sample if requested
                        if save_samples:
                            sample_path = f"data/{client['client_name'].replace(' ', '_')}_content.txt"
                            with open(sample_path, "w", encoding="utf-8") as f:
                                f.write(content[:1000] + "..." if len(content) > 1000 else content)
                            st.info(f"📄 Sample saved to: {sample_path}")
                        
                        # Show content preview if requested
                        if show_content:
                            with st.expander(f"📄 Content Preview - {client['client_name']}"):
                                st.text_area("Scraped Content", content[:500] + "..." if len(content) > 500 else content, height=200)
                    else:
                        failed_scrapes += 1
                        st.error(f"❌ {client['client_name']}: Failed to scrape content")
                        
                except Exception as e:
                    failed_scrapes += 1
                    st.error(f"❌ {client['client_name']}: Error - {str(e)}")
                
                # Update progress
                progress_bar.progress((i + 1) / len(clients_to_scrape))
            
            # Save updated data
            output_path = "data/client_data_with_content.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(client_data, f, indent=2, ensure_ascii=False)
            
            st.success(f"✅ Scraping completed! {successful_scrapes} successful, {failed_scrapes} failed")
            st.markdown(f"**Output saved to:** `{output_path}`")
            
            # Store in session state
            st.session_state.client_data_with_content = client_data
            st.session_state.client_data_with_content_path = output_path

# Display existing scraped data if available
if os.path.exists("data/client_data_with_content.json"):
    st.header("📂 Existing Scraped Data")
    st.markdown("Found existing scraped data:")
    
    try:
        with open("data/client_data_with_content.json", 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        scraped_count = sum(1 for client in existing_data if client.get('landing_page_content'))
        st.success(f"✅ Found {scraped_count}/{len(existing_data)} clients with scraped content")
        
        # Load into session state
        st.session_state.client_data_with_content = existing_data
        st.session_state.client_data_with_content_path = "data/client_data_with_content.json"
        
        # Show preview
        with st.expander("👀 Preview Scraped Data"):
            for client in existing_data:
                has_content = bool(client.get('landing_page_content'))
                status = "✅" if has_content else "❌"
                content_length = len(client.get('landing_page_content', ''))
                st.markdown(f"{status} **{client['client_name']}** - {content_length} characters")
        
    except Exception as e:
        st.error(f"❌ Error loading existing scraped data: {str(e)}")

# Individual client scraping (alternative to batch)
if not scrape_all:
    st.header("🎯 Individual Client Scraping")
    client_names = [client['client_name'] for client in client_data]
    selected_client = st.selectbox("Select client to scrape:", client_names)
    st.session_state.selected_client = selected_client

# Instructions
with st.expander("ℹ️ Instructions"):
    st.markdown("""
    **This step extracts content from client landing pages:**
    - Scrapes text content from client URLs
    - Removes HTML tags and formatting
    - Extracts clean, readable text for analysis
    
    **Process:**
    - Loads parsed client data from previous step
    - Visits each client URL
    - Extracts and cleans text content
    - Saves content samples for review
    
    **Output:**
    - Enhanced JSON data with landing page content
    - Content samples saved as text files
    - Data ready for RAG processing
    """)

# Next steps
st.header("➡️ Next Steps")
st.markdown("""
After scraping landing pages, proceed to:
1. **🧠 RAG Processor** - Build vector database for semantic search
2. **🤖 OpenAI Ad Generator** - Generate AI text campaigns
3. **🎨 Professional Ad Generator** - Create visual ads
""") 