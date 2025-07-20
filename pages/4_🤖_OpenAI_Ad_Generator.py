import streamlit as st
import sys
import os
import json
from pathlib import Path

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

# Import the existing OpenAI ad generation logic
from openai_ad_generator import OpenAIAdGenerator, generate_complete_campaign

# Page configuration
st.set_page_config(
    page_title="OpenAI Ad Generator",
    page_icon="🤖",
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
    .ad-preview {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 OpenAI Ad Generator")
st.markdown("Generate AI text campaigns using GPT-4o with RAG integration")

# Check for processed data
if not os.path.exists("data/processed_client_data_rag.json"):
    st.error("❌ No RAG-processed data found. Please run the RAG Processor step first.")
    st.stop()

# Load processed data
try:
    with open("data/processed_client_data_rag.json", 'r', encoding='utf-8') as f:
        processed_data = json.load(f)
    st.success(f"✅ Loaded processed data for {len(processed_data)} clients")
except Exception as e:
    st.error(f"❌ Error loading processed data: {str(e)}")
    st.stop()

# OpenAI Configuration
st.header("⚙️ OpenAI Configuration")

# API Key input
api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    help="Enter your OpenAI API key. You can also set it in the .env file."
)

# Check for .env file
if os.path.exists(".env"):
    st.info("✅ Found .env file. API key can be loaded from there.")
else:
    st.warning("⚠️ No .env file found. Create one with your OpenAI API key.")

# Model configuration
col1, col2 = st.columns(2)

with col1:
    text_model = st.selectbox(
        "Text Model",
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        help="OpenAI model for text generation"
    )
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

with col2:
    max_tokens = st.slider("Max Tokens", 1000, 8000, 4000, 500)
    use_rag = st.checkbox("Use RAG Integration", value=True, help="Use vector database for enhanced context")

# Client Selection
st.header("🎯 Client Selection")
client_names = list(processed_data.keys())
selected_clients = st.multiselect(
    "Select clients to generate ads for:",
    client_names,
    default=client_names[:2] if len(client_names) >= 2 else client_names,
    help="Choose which clients to generate ad campaigns for"
)

# Generate button
if st.button("🚀 Generate Ad Campaigns", type="primary"):
    if not selected_clients:
        st.warning("⚠️ Please select at least one client.")
    elif not api_key and not os.path.exists(".env"):
        st.warning("⚠️ Please provide an OpenAI API key.")
    else:
        with st.spinner("Generating ad campaigns..."):
            try:
                # Initialize OpenAI ad generator
                generator = OpenAIAdGenerator(api_key=api_key if api_key else None)
                
                # Load RAG processor if requested
                if use_rag:
                    generator.load_rag_processor()
                
                # Generate campaigns for selected clients
                campaigns = []
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, client_name in enumerate(selected_clients):
                    status_text.text(f"Generating ads for {client_name}...")
                    
                    client_data = processed_data[client_name]
                    
                    # Generate campaign for this client
                    campaign = generator.generate_campaign_for_client(client_data)
                    campaigns.append(campaign)
                    
                    progress_bar.progress((i + 1) / len(selected_clients))
                
                # Save campaigns
                output_path = "generated_ads_text/ad_campaigns.json"
                os.makedirs("generated_ads_text", exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(campaigns, f, indent=2, ensure_ascii=False)
                
                st.success(f"✅ Generated ad campaigns for {len(selected_clients)} clients!")
                st.markdown(f"**Output saved to:** `{output_path}`")
                
                # Store in session state
                st.session_state.generated_campaigns = campaigns
                st.session_state.generated_campaigns_path = output_path
                
                # Display results
                st.header("📢 Generated Ad Campaigns")
                
                for campaign in campaigns:
                    client_name = campaign.get('client_name', 'Unknown Client')
                    with st.expander(f"🏢 {client_name}", expanded=True):
                        # LinkedIn Ad
                        if 'linkedin_single_image' in campaign:
                            st.subheader("💼 LinkedIn Single Image Ad")
                            linkedin_ad = campaign['linkedin_single_image']
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Headline:** {linkedin_ad.get('headline', 'N/A')}")
                                st.markdown(f"**Body:** {linkedin_ad.get('body', 'N/A')}")
                            
                            with col2:
                                st.markdown(f"**CTA:** {linkedin_ad.get('call_to_action', 'N/A')}")
                                st.markdown(f"**Image Description:** {linkedin_ad.get('image_description', 'N/A')}")
                        
                        # Banner Ad
                        if 'banner_ad_300x250' in campaign:
                            st.subheader("🖼️ Banner Ad (300x250)")
                            banner_ad = campaign['banner_ad_300x250']
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Headline:** {banner_ad.get('headline', 'N/A')}")
                                st.markdown(f"**Body:** {banner_ad.get('body', 'N/A')}")
                            
                            with col2:
                                st.markdown(f"**CTA:** {banner_ad.get('call_to_action', 'N/A')}")
                                st.markdown(f"**Image Description:** {banner_ad.get('image_description', 'N/A')}")
                        
                        # Additional Creative
                        if 'additional_creative' in campaign:
                            st.subheader("🎨 Additional Creative")
                            additional_ad = campaign['additional_creative']
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Headline:** {additional_ad.get('headline', 'N/A')}")
                                st.markdown(f"**Body:** {additional_ad.get('body', 'N/A')}")
                            
                            with col2:
                                st.markdown(f"**CTA:** {additional_ad.get('call_to_action', 'N/A')}")
                                st.markdown(f"**Image Description:** {additional_ad.get('image_description', 'N/A')}")
                        
                        # News Connection
                        if 'news_connection_rationale' in campaign:
                            st.markdown(f"**📰 News Connection:** {campaign['news_connection_rationale']}")
                
            except Exception as e:
                st.error(f"❌ Error generating ad campaigns: {str(e)}")
                st.exception(e)

# Display existing generated campaigns if available
if os.path.exists("generated_ads_text/ad_campaigns.json"):
    st.header("📂 Existing Generated Campaigns")
    st.markdown("Found existing ad campaigns:")
    
    try:
        with open("generated_ads_text/ad_campaigns.json", 'r', encoding='utf-8') as f:
            existing_campaigns = json.load(f)
        
        st.success(f"✅ Found {len(existing_campaigns)} generated campaigns")
        
        # Load into session state
        st.session_state.generated_campaigns = existing_campaigns
        st.session_state.generated_campaigns_path = "generated_ads_text/ad_campaigns.json"
        
        # Show preview
        with st.expander("👀 Preview Generated Campaigns"):
            for campaign in existing_campaigns[:2]:  # Show first 2 campaigns
                client_name = campaign.get('client_name', 'Unknown Client')
                st.markdown(f"**{client_name}**")
                
                if 'linkedin_single_image' in campaign:
                    headline = campaign['linkedin_single_image'].get('headline', 'N/A')
                    st.markdown(f"  LinkedIn: {headline[:60]}...")
        
    except Exception as e:
        st.error(f"❌ Error loading existing campaigns: {str(e)}")

# Individual client generation (alternative to batch)
st.header("🎯 Individual Client Generation")
if selected_clients:
    individual_client = st.selectbox("Select client for individual generation:", selected_clients)
    
    if st.button("🎯 Generate for Selected Client", type="secondary"):
        if individual_client and (api_key or os.path.exists(".env")):
            with st.spinner(f"Generating ads for {individual_client}..."):
                try:
                    generator = OpenAIAdGenerator(api_key=api_key if api_key else None)
                    
                    if use_rag:
                        generator.load_rag_processor()
                    
                    client_data = processed_data[individual_client]
                    campaign = generator.generate_campaign_for_client(client_data)
                    
                    st.success(f"✅ Generated campaign for {individual_client}")
                    
                    # Display the campaign
                    st.subheader(f"📢 Campaign for {individual_client}")
                    st.json(campaign)
                    
                except Exception as e:
                    st.error(f"❌ Error generating campaign: {str(e)}")
        else:
            st.warning("⚠️ Please select a client and provide API key.")

# Instructions
with st.expander("ℹ️ Instructions"):
    st.markdown("""
    **This step generates AI-powered ad campaigns:**
    - Uses OpenAI GPT-4o for text generation
    - Integrates with RAG system for context-aware content
    - Generates multiple ad formats (LinkedIn, banner, additional)
    
    **Process:**
    - Loads RAG-processed client data
    - Uses semantic search to find relevant news
    - Generates professional, compliant ad copy
    - Connects client expertise with current news themes
    
    **Output:**
    - Structured JSON with ad campaigns
    - Multiple ad formats per client
    - Ready for visual ad generation
    """)

# Next steps
st.header("➡️ Next Steps")
st.markdown("""
After generating text campaigns, proceed to:
1. **🎨 Professional Ad Generator** - Create complete visual ads with DALL-E 3
""") 