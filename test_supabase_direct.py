#!/usr/bin/env python3
"""
Direct Supabase test to verify table creation and basic operations
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def test_supabase_direct():
    """Test Supabase connection and table operations"""
    try:
        # Initialize Supabase client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        print(f"Testing connection to: {supabase_url}")
        
        client = create_client(supabase_url, supabase_key)
        
        # Try to insert a test record
        test_data = {
            'plate_number': 'TEST123',
            'confidence_score': 0.95,
            'camera_location': 'Test Location'
        }
        
        print("Inserting test record...")
        result = client.table('license_plates').insert(test_data).execute()
        
        if result.data:
            record_id = result.data[0]['id']
            print(f"✅ Successfully inserted test record with ID: {record_id}")
            
            # Try to retrieve the record
            print("Retrieving test record...")
            retrieve_result = client.table('license_plates').select('*').eq('id', record_id).execute()
            
            if retrieve_result.data:
                print(f"✅ Successfully retrieved record: {retrieve_result.data[0]}")
                
                # Clean up - delete the test record
                print("Cleaning up test record...")
                delete_result = client.table('license_plates').delete().eq('id', record_id).execute()
                print("✅ Test record deleted")
                
                return True
            else:
                print("❌ Failed to retrieve record")
                return False
        else:
            print("❌ Failed to insert record")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_direct()
    if success:
        print("\n🎉 Supabase is working perfectly!")
        print("Your LPR system is ready to use!")
    else:
        print("\n⚠️  Supabase needs configuration")
