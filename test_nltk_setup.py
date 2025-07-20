#!/usr/bin/env python3
"""
Test script to verify NLTK setup for News-Responsive Ad Generation
"""

import sys
import os
from pathlib import Path

def test_nltk_setup():
    """Test NLTK installation and data download"""
    print("🧪 Testing NLTK setup...")
    
    # Test 1: Check if NLTK is installed
    try:
        import nltk
        print("✅ NLTK is installed")
    except ImportError:
        print("❌ NLTK is not installed")
        return False
    
    # Test 2: Check if stopwords are available
    try:
        nltk.data.find('corpora/stopwords')
        print("✅ NLTK stopwords are available")
        stopwords_available = True
    except LookupError:
        print("⚠️ NLTK stopwords not found, downloading...")
        try:
            nltk.download('stopwords', quiet=True)
            print("✅ NLTK stopwords downloaded successfully")
            stopwords_available = True
        except Exception as e:
            print(f"❌ Failed to download stopwords: {e}")
            stopwords_available = False
    
    # Test 3: Check if punkt is available
    try:
        nltk.data.find('tokenizers/punkt')
        print("✅ NLTK punkt is available")
        punkt_available = True
    except LookupError:
        print("⚠️ NLTK punkt not found, downloading...")
        try:
            nltk.download('punkt', quiet=True)
            print("✅ NLTK punkt downloaded successfully")
            punkt_available = True
        except Exception as e:
            print(f"❌ Failed to download punkt: {e}")
            punkt_available = False
    
    # Test 4: Test RAKE functionality
    if stopwords_available and punkt_available:
        try:
            from rake_nltk import Rake
            rake = Rake()
            test_text = "This is a test sentence for keyword extraction."
            rake.extract_keywords_from_text(test_text)
            keywords = rake.get_ranked_phrases()
            print(f"✅ RAKE keyword extraction works: {keywords[:3]}")
            return True
        except Exception as e:
            print(f"❌ RAKE test failed: {e}")
            return False
    else:
        print("❌ Cannot test RAKE - missing NLTK data")
        return False

def test_rag_processor():
    """Test RAG processor initialization"""
    print("\n🧪 Testing RAG processor...")
    
    try:
        # Add utils to path
        sys.path.append(str(Path(__file__).parent / "utils"))
        
        from rag_processor import RAGProcessor
        
        # Initialize RAG processor
        rag = RAGProcessor()
        print("✅ RAG processor initialized successfully")
        
        # Test keyword extraction
        test_text = "This is a test sentence for keyword extraction using RAKE algorithm."
        keywords = rag.extract_keywords(test_text)
        print(f"✅ Keyword extraction works: {keywords}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG processor test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 NLTK Setup Test for News-Responsive Ad Generation")
    print("=" * 60)
    
    # Test NLTK setup
    nltk_ok = test_nltk_setup()
    
    # Test RAG processor
    rag_ok = test_rag_processor()
    
    print("\n" + "=" * 60)
    if nltk_ok and rag_ok:
        print("🎉 All tests passed! NLTK setup is working correctly.")
        print("   You can now run the RAG processor without issues.")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("   You may need to manually install NLTK data:")
        print("   python -c \"import nltk; nltk.download('stopwords'); nltk.download('punkt')\"") 