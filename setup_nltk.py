#!/usr/bin/env python3
"""
NLTK Data Setup Script for News-Responsive Ad Generation
Downloads required NLTK data for RAG processing
"""

import os
import sys
import subprocess

def install_nltk():
    """Install NLTK if not already installed"""
    try:
        import nltk
        print("✅ NLTK is already installed")
        return True
    except ImportError:
        print("📦 Installing NLTK...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
            print("✅ NLTK installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install NLTK")
            return False

def setup_nltk_data():
    """Download required NLTK data"""
    # First ensure NLTK is installed
    if not install_nltk():
        return
    
    import nltk
    
    print("🔧 Setting up NLTK data for RAG processing...")
    
    # Required NLTK data
    required_data = ['stopwords', 'punkt']
    
    for data_name in required_data:
        try:
            print(f"📥 Downloading {data_name}...")
            nltk.download(data_name, quiet=True)
            print(f"✅ {data_name} downloaded successfully")
        except Exception as e:
            print(f"❌ Error downloading {data_name}: {e}")
            
            # Try alternative download location
            try:
                print(f"🔄 Trying alternative download location for {data_name}...")
                nltk.download(data_name, download_dir='./nltk_data', quiet=True)
                print(f"✅ {data_name} downloaded to ./nltk_data/")
            except Exception as e2:
                print(f"❌ Failed to download {data_name}: {e2}")
                print(f"   Please download manually: python -c 'import nltk; nltk.download(\"{data_name}\")'")
    
    print("\n🎉 NLTK setup complete!")
    print("   You can now run the RAG processor without NLTK errors.")

def setup_nltk_data():
    """Download required NLTK data"""
    print("🔧 Setting up NLTK data for RAG processing...")
    
    # Required NLTK data
    required_data = ['stopwords', 'punkt']
    
    for data_name in required_data:
        try:
            print(f"📥 Downloading {data_name}...")
            nltk.download(data_name, quiet=True)
            print(f"✅ {data_name} downloaded successfully")
        except Exception as e:
            print(f"❌ Error downloading {data_name}: {e}")
            
            # Try alternative download location
            try:
                print(f"🔄 Trying alternative download location for {data_name}...")
                nltk.download(data_name, download_dir='./nltk_data', quiet=True)
                print(f"✅ {data_name} downloaded to ./nltk_data/")
            except Exception as e2:
                print(f"❌ Failed to download {data_name}: {e2}")
                print(f"   Please download manually: python -c 'import nltk; nltk.download(\"{data_name}\")'")
    
    print("\n🎉 NLTK setup complete!")
    print("   You can now run the RAG processor without NLTK errors.")

if __name__ == "__main__":
    setup_nltk_data() 