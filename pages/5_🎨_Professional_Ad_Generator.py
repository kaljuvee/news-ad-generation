import streamlit as st
import sys
import os
import json
from pathlib import Path

# Add utils directory to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

# Import the existing professional ad generation logic
from professional_ad_generator import ProfessionalAdGenerator

# Page configuration
st.set_page_config(
    page_title="Professional Ad Generator",
    page_icon="🎨",
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
    .image-preview {
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🎨 Professional Ad Generator")
st.markdown("Create complete visual ads with DALL-E 3 and text overlays")

# Check for generated campaigns
if not os.path.exists("generated_ads_text/ad_campaigns.json"):
    st.error("❌ No generated ad campaigns found. Please run the OpenAI Ad Generator step first.")
    st.stop()

# Load generated campaigns
try:
    with open("generated_ads_text/ad_campaigns.json", 'r', encoding='utf-8') as f:
        generated_campaigns = json.load(f)
    st.success(f"✅ Loaded {len(generated_campaigns)} generated campaigns")
except Exception as e:
    st.error(f"❌ Error loading generated campaigns: {str(e)}")
    st.stop()

# OpenAI Configuration
st.header("⚙️ OpenAI Configuration")

# API Key input
api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    help="Enter your OpenAI API key for DALL-E 3 image generation. You can also set it in the .env file."
)

# Check for .env file
if os.path.exists(".env"):
    st.info("✅ Found .env file. API key can be loaded from there.")
else:
    st.warning("⚠️ No .env file found. Create one with your OpenAI API key.")

# Image Generation Configuration
st.header("🎨 Image Generation Settings")
col1, col2 = st.columns(2)

with col1:
    image_quality = st.selectbox(
        "Image Quality",
        ["hd", "standard"],
        help="DALL-E 3 image quality setting"
    )
    
    image_size_linkedin = st.selectbox(
        "LinkedIn Image Size",
        ["1024x1024", "1792x1024"],
        help="Size for LinkedIn single image ads"
    )

with col2:
    image_size_banner = st.selectbox(
        "Banner Image Size",
        ["1792x1024", "1024x1024"],
        help="Size for banner ads"
    )
    
    save_backgrounds = st.checkbox("Save Background Images", value=True, help="Save background images separately")

# Client Selection
st.header("🎯 Client Selection")
client_names = [campaign.get('client_name', 'Unknown Client') for campaign in generated_campaigns]
selected_clients = st.multiselect(
    "Select clients to generate visual ads for:",
    client_names,
    default=client_names[:2] if len(client_names) >= 2 else client_names,
    help="Choose which clients to generate visual ads for"
)

# Ad Format Selection
st.header("📐 Ad Format Selection")
ad_formats = st.multiselect(
    "Select ad formats to generate:",
    ["linkedin_single_image", "banner_ad_300x250", "additional_creative"],
    default=["linkedin_single_image", "banner_ad_300x250"],
    help="Choose which ad formats to generate"
)

# Generate button
if st.button("🚀 Generate Visual Ads", type="primary"):
    if not selected_clients:
        st.warning("⚠️ Please select at least one client.")
    elif not ad_formats:
        st.warning("⚠️ Please select at least one ad format.")
    elif not api_key and not os.path.exists(".env"):
        st.warning("⚠️ Please provide an OpenAI API key for image generation.")
    else:
        with st.spinner("Generating visual ads..."):
            try:
                # Initialize professional ad generator
                generator = ProfessionalAdGenerator(api_key=api_key if api_key else None)
                
                # Move data files to organized structure
                generator.move_data_files()
                
                # Filter campaigns for selected clients
                selected_campaigns = [c for c in generated_campaigns if c.get('client_name') in selected_clients]
                
                # Generate visual ads
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_ads = len(selected_campaigns) * len(ad_formats)
                current_ad = 0
                
                generated_images = []
                
                for campaign in selected_campaigns:
                    client_name = campaign.get('client_name', 'Unknown Client')
                    
                    for ad_format in ad_formats:
                        if ad_format in campaign:
                            status_text.text(f"Generating {ad_format} for {client_name}...")
                            
                            ad_data = campaign[ad_format]
                            
                            # Generate complete ad
                            success = generator.generate_complete_ad_campaign_for_client(
                                client_name, ad_data, ad_format
                            )
                            
                            if success:
                                generated_images.append({
                                    'client_name': client_name,
                                    'ad_format': ad_format,
                                    'ad_data': ad_data
                                })
                            
                            current_ad += 1
                            progress_bar.progress(current_ad / total_ads)
                
                st.success(f"✅ Generated visual ads for {len(selected_clients)} clients!")
                
                # Display results
                st.header("🖼️ Generated Visual Ads")
                
                # Show generated images
                if os.path.exists("generated_ads_images/final_ads"):
                    image_files = [f for f in os.listdir("generated_ads_images/final_ads") if f.endswith('.png')]
                    
                    if image_files:
                        st.success(f"✅ Found {len(image_files)} generated ad images")
                        
                        # Group by client
                        for client_name in selected_clients:
                            client_images = [f for f in image_files if client_name.replace(' ', '_') in f]
                            
                            if client_images:
                                with st.expander(f"🏢 {client_name} - {len(client_images)} ads", expanded=True):
                                    # Display images in columns
                                    cols = st.columns(min(3, len(client_images)))
                                    
                                    for i, image_file in enumerate(client_images):
                                        col_idx = i % 3
                                        with cols[col_idx]:
                                            image_path = f"generated_ads_images/final_ads/{image_file}"
                                            st.image(image_path, caption=image_file, use_column_width=True)
                                            
                                            # Add download button
                                            with open(image_path, "rb") as file:
                                                st.download_button(
                                                    label=f"Download {image_file}",
                                                    data=file.read(),
                                                    file_name=image_file,
                                                    mime="image/png"
                                                )
                    else:
                        st.warning("⚠️ No generated images found.")
                
                # Store in session state
                st.session_state.generated_images = generated_images
                
            except Exception as e:
                st.error(f"❌ Error generating visual ads: {str(e)}")
                st.exception(e)

# Display existing generated images if available
if os.path.exists("generated_ads_images/final_ads"):
    st.header("📂 Existing Generated Images")
    
    image_files = [f for f in os.listdir("generated_ads_images/final_ads") if f.endswith('.png')]
    
    if image_files:
        st.success(f"✅ Found {len(image_files)} existing ad images")
        
        # Show image gallery
        with st.expander("🖼️ Image Gallery", expanded=False):
            # Group by client
            client_groups = {}
            for image_file in image_files:
                # Extract client name from filename
                parts = image_file.split('_')
                if len(parts) >= 2:
                    client_name = parts[0]
                    if client_name not in client_groups:
                        client_groups[client_name] = []
                    client_groups[client_name].append(image_file)
            
            for client_name, images in client_groups.items():
                st.subheader(f"🏢 {client_name}")
                
                # Display images in rows
                for i in range(0, len(images), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(images):
                            with cols[j]:
                                image_path = f"generated_ads_images/final_ads/{images[i+j]}"
                                st.image(image_path, caption=images[i+j], use_column_width=True)
    else:
        st.info("📂 No existing images found in the final_ads directory.")

# Individual client generation (alternative to batch)
st.header("🎯 Individual Client Generation")
if selected_clients:
    individual_client = st.selectbox("Select client for individual generation:", selected_clients)
    individual_format = st.selectbox("Select ad format:", ad_formats)
    
    if st.button("🎯 Generate for Selected Client", type="secondary"):
        if individual_client and individual_format and (api_key or os.path.exists(".env")):
            with st.spinner(f"Generating {individual_format} for {individual_client}..."):
                try:
                    # Find the campaign for this client
                    campaign = next((c for c in generated_campaigns if c.get('client_name') == individual_client), None)
                    
                    if campaign and individual_format in campaign:
                        generator = ProfessionalAdGenerator(api_key=api_key if api_key else None)
                        
                        ad_data = campaign[individual_format]
                        success = generator.generate_complete_ad_campaign_for_client(
                            individual_client, ad_data, individual_format
                        )
                        
                        if success:
                            st.success(f"✅ Generated {individual_format} for {individual_client}")
                            
                            # Show the generated image
                            image_files = [f for f in os.listdir("generated_ads_images/final_ads") 
                                         if f.endswith('.png') and individual_client.replace(' ', '_') in f 
                                         and individual_format.replace('_', '') in f]
                            
                            if image_files:
                                latest_image = image_files[-1]  # Get the most recent
                                image_path = f"generated_ads_images/final_ads/{latest_image}"
                                st.image(image_path, caption=latest_image, use_column_width=True)
                        else:
                            st.error(f"❌ Failed to generate {individual_format} for {individual_client}")
                    else:
                        st.warning(f"⚠️ No {individual_format} data found for {individual_client}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating individual ad: {str(e)}")
        else:
            st.warning("⚠️ Please select a client, format, and provide API key.")

# Instructions
with st.expander("ℹ️ Instructions"):
    st.markdown("""
    **This step creates complete visual ad campaigns:**
    - Uses DALL-E 3 HD for background image generation
    - Adds professional text overlays with PIL
    - Creates multiple ad formats (LinkedIn, banner, additional)
    - Organizes output in structured folders
    
    **Process:**
    - Loads generated text campaigns
    - Generates background images with DALL-E 3
    - Adds text overlays with professional typography
    - Saves complete marketing-ready ads
    
    **Output:**
    - Complete visual ad campaigns
    - Multiple formats per client
    - Marketing-ready PNG files
    - Organized folder structure
    """)

# Final summary
st.header("🎉 Pipeline Complete!")
st.markdown("""
Congratulations! You've successfully completed the entire news-responsive ad generation pipeline:

1. ✅ **Parse Client Data** - Extracted client information and news articles
2. ✅ **Web Scraping** - Collected landing page content
3. ✅ **RAG Processing** - Built vector database for semantic search
4. ✅ **AI Text Generation** - Created context-aware ad copy
5. ✅ **Visual Ad Generation** - Produced complete marketing materials

**Your generated ads are now ready for deployment!** 🚀
""")

# Download all results
if os.path.exists("generated_ads_images/final_ads"):
    st.header("📥 Download Results")
    
    # Create zip file of all generated ads
    import zipfile
    import io
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk("generated_ads_images"):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, "generated_ads_images")
                zip_file.write(file_path, arc_name)
    
    st.download_button(
        label="📦 Download All Generated Ads (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="generated_ad_campaigns.zip",
        mime="application/zip"
    ) 