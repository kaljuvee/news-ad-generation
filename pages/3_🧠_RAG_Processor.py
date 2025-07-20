import streamlit as st
import sys
import os
import json
from pathlib import Path

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

# Import the existing RAG processing logic and Streamlit setup
from rag_processor import RAGProcessor, process_client_data_with_rag
from streamlit_setup import setup_nltk_for_streamlit

# Page configuration
st.set_page_config(
    page_title="RAG Processor",
    page_icon="🧠",
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
st.title("🧠 RAG Processor")
st.markdown("Build vector database and perform semantic search for news relevance")

# Setup NLTK for RAG processing
if 'nltk_setup_complete' not in st.session_state:
    st.info("🔧 Setting up NLTK data for RAG processing...")
    if setup_nltk_for_streamlit():
        st.session_state.nltk_setup_complete = True
    else:
        st.error("❌ NLTK setup failed. Please check the error messages above.")
        st.stop()

# Check for scraped data
if not os.path.exists("data/client_data_with_content.json"):
    st.error("❌ No scraped client data found. Please run the Web Scraper step first.")
    st.stop()

# Load scraped data
try:
    with open("data/client_data_with_content.json", 'r', encoding='utf-8') as f:
        client_data = json.load(f)
    st.success(f"✅ Loaded {len(client_data)} clients from scraped data")
except Exception as e:
    st.error(f"❌ Error loading scraped data: {str(e)}")
    st.stop()

# RAG Configuration
st.header("⚙️ RAG Configuration")
col1, col2 = st.columns(2)

with col1:
    model_name = st.selectbox(
        "Embedding Model",
        ["all-MiniLM-L6-v2", "all-mpnet-base-v2", "paraphrase-multilingual-MiniLM-L12-v2"],
        help="SentenceTransformer model for generating embeddings"
    )
    
    max_keywords = st.slider("Max Keywords per Text", 3, 10, 5)

with col2:
    chunk_size = st.slider("Text Chunk Size", 256, 1024, 512, step=128)
    top_k_results = st.slider("Top K Search Results", 3, 15, 5)

# Process button
if st.button("🚀 Build Vector Database", type="primary"):
    with st.spinner("Building vector database..."):
        try:
            # Initialize RAG processor
            rag_processor = RAGProcessor(model_name=model_name)
            
            # Build vector database
            rag_processor.build_vector_database(client_data)
            
            # Process client data with RAG
            processed_data = process_client_data_with_rag("data/client_data_with_content.json")
            
            # Save processed data
            output_path = "data/processed_client_data_rag.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2, ensure_ascii=False)
            
            st.success("✅ Vector database built successfully!")
            st.markdown(f"**Output saved to:** `{output_path}`")
            
            # Store in session state
            st.session_state.rag_processor = rag_processor
            st.session_state.processed_data = processed_data
            st.session_state.processed_data_path = output_path
            
            # Display statistics
            st.header("📊 Vector Database Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Embeddings", len(rag_processor.metadata))
            
            with col2:
                st.metric("Embedding Dimension", rag_processor.dimension)
            
            with col3:
                st.metric("Model Used", model_name)
            
        except Exception as e:
            st.error(f"❌ Error building vector database: {str(e)}")
            st.exception(e)

# Semantic Search Interface
st.header("🔍 Semantic Search")
st.markdown("Test semantic search functionality:")

# Search options
col1, col2 = st.columns(2)

with col1:
    search_query = st.text_area(
        "Search Query",
        placeholder="Enter your search query...",
        help="Enter a query to find relevant content"
    )
    
    search_type = st.selectbox(
        "Content Type Filter",
        ["All", "landing_page", "news_article"],
        help="Filter results by content type"
    )

with col2:
    num_results = st.slider("Number of Results", 3, 10, 5)
    
    if st.button("🔍 Search", type="secondary"):
        if search_query and hasattr(st.session_state, 'rag_processor'):
            with st.spinner("Performing semantic search..."):
                try:
                    rag_processor = st.session_state.rag_processor
                    
                    # Perform search
                    filter_type = None if search_type == "All" else search_type
                    results = rag_processor.semantic_search(
                        search_query, 
                        k=num_results, 
                        filter_type=filter_type
                    )
                    
                    # Display results
                    st.subheader("🔍 Search Results")
                    for i, result in enumerate(results):
                        with st.expander(f"Result {i+1} - Score: {result['similarity_score']:.3f}", expanded=(i==0)):
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                st.markdown(f"**Type:** {result['type']}")
                                if result['type'] == 'landing_page':
                                    st.markdown(f"**Client:** {result['client_name']}")
                                else:
                                    st.markdown(f"**Source:** {result.get('source', 'N/A')}")
                            
                            with col2:
                                if result['type'] == 'landing_page':
                                    st.markdown(f"**Content:** {result['content'][:200]}...")
                                else:
                                    st.markdown(f"**Title:** {result.get('title', 'N/A')}")
                                    st.markdown(f"**Content:** {result['content'][:200]}...")
                            
                            st.markdown(f"**Keywords:** {', '.join(result.get('keywords', [])[:5])}")
                            
                except Exception as e:
                    st.error(f"❌ Error performing search: {str(e)}")
        else:
            st.warning("⚠️ Please enter a search query and ensure vector database is built.")

# Display existing processed data if available
if os.path.exists("data/processed_client_data_rag.json"):
    st.header("📂 Existing Processed Data")
    st.markdown("Found existing RAG-processed data:")
    
    try:
        with open("data/processed_client_data_rag.json", 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        st.success(f"✅ Found processed data for {len(existing_data)} clients")
        
        # Load into session state
        st.session_state.processed_data = existing_data
        st.session_state.processed_data_path = "data/processed_client_data_rag.json"
        
        # Show preview
        with st.expander("👀 Preview Processed Data"):
            for client_name, client_data in existing_data.items():
                relevant_news_count = len(client_data.get('relevant_news', []))
                st.markdown(f"**{client_name}** - {relevant_news_count} relevant news articles")
                
                # Show top relevant news
                if relevant_news_count > 0:
                    top_news = client_data['relevant_news'][0]
                    st.markdown(f"  Top: {top_news.get('title', 'N/A')[:60]}... (Score: {top_news.get('similarity_score', 0):.3f})")
        
    except Exception as e:
        st.error(f"❌ Error loading existing processed data: {str(e)}")

# Vector Database Status
st.header("🗄️ Vector Database Status")
if os.path.exists("data/vector_index.faiss") and os.path.exists("data/vector_metadata.pkl"):
    st.success("✅ Vector database files found")
    
    # Load and display database info
    try:
        rag_processor = RAGProcessor()
        if rag_processor.load_index():
            st.info(f"📊 Database contains {len(rag_processor.metadata)} embeddings")
            st.info(f"🔢 Embedding dimension: {rag_processor.dimension}")
            
            # Store in session state
            st.session_state.rag_processor = rag_processor
        else:
            st.warning("⚠️ Could not load vector database")
    except Exception as e:
        st.error(f"❌ Error loading vector database: {str(e)}")
else:
    st.warning("⚠️ No vector database files found. Build the database first.")

# Instructions
with st.expander("ℹ️ Instructions"):
    st.markdown("""
    **This step builds a vector database for semantic search:**
    - Creates embeddings for landing page content and news articles
    - Builds FAISS index for fast similarity search
    - Enables finding relevant news for each client
    
    **Process:**
    - Loads scraped client data
    - Generates embeddings using SentenceTransformer
    - Builds FAISS vector index
    - Performs semantic search to find relevant news
    
    **Output:**
    - FAISS vector index and metadata
    - Processed data with relevant news for each client
    - Ready for AI ad generation
    """)

# Next steps
st.header("➡️ Next Steps")
st.markdown("""
After building the vector database, proceed to:
1. **🤖 OpenAI Ad Generator** - Generate AI text campaigns
2. **🎨 Professional Ad Generator** - Create visual ads
""") 