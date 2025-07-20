#!/usr/bin/env python3
"""
Test script to verify JSON serialization fix for RAG processor
"""

import json
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent / "utils"))

def test_json_serialization():
    """Test that processed data can be serialized to JSON"""
    print("🧪 Testing JSON serialization...")
    
    try:
        from rag_processor import process_client_data_with_rag
        
        # Test with sample data
        sample_data = [
            {
                'client_name': 'Test Client',
                'url': 'https://example.com',
                'landing_page_content': 'This is a test landing page content for keyword extraction.',
                'news_articles': [
                    {
                        'title': 'Test News Article',
                        'source': 'Test Source',
                        'published_date': '2024-01-01',
                        'url': 'https://example.com/news'
                    }
                ]
            }
        ]
        
        # Save sample data
        with open('test_client_data.json', 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        # Process with RAG
        print("📊 Processing sample data with RAG...")
        processed_data = process_client_data_with_rag('test_client_data.json')
        
        # Test JSON serialization
        print("💾 Testing JSON serialization...")
        json_string = json.dumps(processed_data, indent=2, ensure_ascii=False)
        
        # Test saving to file
        with open('test_processed_data.json', 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print("✅ JSON serialization successful!")
        print(f"📁 Processed data saved to test_processed_data.json")
        
        # Show structure
        print(f"\n📋 Data structure:")
        for client_name, client_data in processed_data.items():
            print(f"  {client_name}:")
            print(f"    - Keywords: {len(client_data.get('landing_page_keywords', []))}")
            print(f"    - Relevant news: {len(client_data.get('relevant_news', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 JSON Serialization Test for RAG Processor")
    print("=" * 50)
    
    success = test_json_serialization()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 JSON serialization test passed!")
        print("   The RAG processor now returns serializable data.")
    else:
        print("❌ JSON serialization test failed.")
        print("   Please check the error messages above.") 