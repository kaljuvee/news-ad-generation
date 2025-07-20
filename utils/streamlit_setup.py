"""
Streamlit-specific setup utilities for News-Responsive Ad Generation
Handles NLTK data download and other setup requirements for Streamlit Cloud
"""

import os
import sys
import subprocess
import streamlit as st
from pathlib import Path

def setup_nltk_for_streamlit():
    """
    Setup NLTK data for Streamlit Cloud deployment
    Downloads required NLTK data to a local directory
    """
    try:
        import nltk
        
        # Check if NLTK data already exists
        try:
            nltk.data.find('corpora/stopwords')
            st.success("✅ NLTK data already available")
            return True
        except LookupError:
            pass
        
        # Create local NLTK data directory
        download_dir = Path.cwd() / 'nltk_data'
        download_dir.mkdir(exist_ok=True)
        
        with st.spinner("📥 Downloading NLTK data for RAG processing..."):
            # Download required NLTK data
            required_data = ['stopwords', 'punkt']
            
            for data_name in required_data:
                try:
                    nltk.download(data_name, download_dir=str(download_dir), quiet=True)
                    st.success(f"✅ Downloaded {data_name}")
                except Exception as e:
                    st.error(f"❌ Failed to download {data_name}: {e}")
                    return False
        
        st.success("🎉 NLTK setup complete!")
        return True
        
    except ImportError:
        st.error("❌ NLTK not installed. Please install it first: pip install nltk")
        return False

def check_dependencies():
    """
    Check if all required dependencies are installed
    """
    required_packages = [
        'pandas', 'openpyxl', 'requests', 'beautifulsoup4',
        'sentence_transformers', 'rake_nltk', 'nltk', 'faiss',
        'openai', 'sklearn', 'dotenv', 'streamlit', 'PIL', 'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'dotenv':
                import dotenv
            elif package == 'sklearn':
                import sklearn
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        st.error(f"❌ Missing packages: {', '.join(missing_packages)}")
        st.info("Please install missing packages: pip install -r requirements.txt")
        return False
    
    st.success("✅ All dependencies are installed")
    return True

def setup_streamlit_environment():
    """
    Complete setup for Streamlit environment
    """
    st.header("🔧 Environment Setup")
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Setup NLTK
    if not setup_nltk_for_streamlit():
        return False
    
    st.success("🎉 Environment setup complete!")
    return True

def get_nltk_data_path():
    """
    Get the path to NLTK data directory
    """
    # Try local directory first
    local_path = Path.cwd() / 'nltk_data'
    if local_path.exists():
        return str(local_path)
    
    # Fallback to default NLTK data path
    try:
        import nltk
        return nltk.data.path[0] if nltk.data.path else None
    except:
        return None 