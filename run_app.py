#!/usr/bin/env python3
"""
Streamlit App Runner for News-Responsive Ad Generation
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Streamlit app"""
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Set up environment
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    # Create necessary directories
    for dir_name in ["data", "generated_ads_text", "generated_ads_images", "generated_ads_images/final_ads"]:
        Path(dir_name).mkdir(exist_ok=True)
    
    # Check and setup NLTK data
    try:
        import nltk
        nltk.data.find('corpora/stopwords')
        print("✅ NLTK data found")
    except LookupError:
        print("📥 NLTK data not found. Setting up...")
        try:
            subprocess.run([sys.executable, "setup_nltk.py"], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ NLTK setup failed. You may need to run it manually:")
            print("   python setup_nltk.py")
    
    print("🚀 Starting Streamlit app...")
    print("📱 Open your browser to: http://localhost:8501")
    print("📋 Use the sidebar to navigate through the pipeline steps")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "Home.py",
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false"
    ])

if __name__ == "__main__":
    main() 