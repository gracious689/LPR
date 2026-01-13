from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict, Optional

load_dotenv()

class SupabaseManager:
    def __init__(self):
        self.supabase: Client = self._connect()
    
    def _connect(self) -> Client:
        """Establish Supabase connection"""
        try:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            
            if not supabase_url or not supabase_key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
            
            client = create_client(supabase_url, supabase_key)
            print("Successfully connected to Supabase")
            return client
            
        except Exception as e:
            print(f"Error connecting to Supabase: {e}")
            raise
    
    def insert_plate_record(self, plate_number: str, confidence_score: Optional[float] = None, 
                          image_path: Optional[str] = None, camera_location: Optional[str] = None) -> Optional[int]:
        """Insert a new license plate record into Supabase"""
        try:
            record_data = {
                'plate_number': plate_number.upper(),
                'confidence_score': confidence_score,
                'image_path': image_path,
                'camera_location': camera_location
            }
            
            # Remove None values
            record_data = {k: v for k, v in record_data.items() if v is not None}
            
            result = self.supabase.table('license_plates').insert(record_data).execute()
            
            if result.data:
                record_id = result.data[0]['id']
                print(f"Successfully inserted plate {plate_number} with ID: {record_id}")
                return record_id
            else:
                print(f"Failed to insert plate {plate_number}")
                return None
                
        except Exception as e:
            print(f"Error inserting plate record: {e}")
            return None
    
    def get_plate_records(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent license plate records"""
        try:
            result = (self.supabase.table('license_plates')
                     .select('*')
                     .order('timestamp', desc=True)
                     .limit(limit)
                     .execute())
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"Error retrieving plate records: {e}")
            return []
    
    def search_plate(self, plate_number: str) -> List[Dict]:
        """Search for specific plate number in Supabase"""
        try:
            result = (self.supabase.table('license_plates')
                     .select('*')
                     .eq('plate_number', plate_number.upper())
                     .order('timestamp', desc=True)
                     .execute())
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"Error searching plate: {e}")
            return []
    
    def get_plates_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get plates within a date range"""
        try:
            result = (self.supabase.table('license_plates')
                     .select('*')
                     .gte('timestamp', start_date)
                     .lte('timestamp', end_date)
                     .order('timestamp', desc=True)
                     .execute())
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"Error retrieving plates by date range: {e}")
            return []
    
    def get_unique_plate_count(self) -> int:
        """Get count of unique license plates"""
        try:
            result = (self.supabase.table('license_plates')
                     .select('plate_number')
                     .execute())
            
            if result.data:
                unique_plates = set(record['plate_number'] for record in result.data)
                return len(unique_plates)
            return 0
            
        except Exception as e:
            print(f"Error getting unique plate count: {e}")
            return 0
    
    def delete_plate_record(self, record_id: int) -> bool:
        """Delete a specific plate record"""
        try:
            result = self.supabase.table('license_plates').delete().eq('id', record_id).execute()
            
            if result.data:
                print(f"Successfully deleted record with ID: {record_id}")
                return True
            else:
                print(f"No record found with ID: {record_id}")
                return False
                
        except Exception as e:
            print(f"Error deleting plate record: {e}")
            return False
    
    def update_plate_record(self, record_id: int, update_data: Dict) -> bool:
        """Update a specific plate record"""
        try:
            result = (self.supabase.table('license_plates')
                     .update(update_data)
                     .eq('id', record_id)
                     .execute())
            
            if result.data:
                print(f"Successfully updated record with ID: {record_id}")
                return True
            else:
                print(f"No record found with ID: {record_id}")
                return False
                
        except Exception as e:
            print(f"Error updating plate record: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test the Supabase connection"""
        try:
            result = self.supabase.table('license_plates').select('count').execute()
            print("✓ Supabase connection test successful!")
            return True
        except Exception as e:
            print(f"✗ Supabase connection test failed: {e}")
            return False
