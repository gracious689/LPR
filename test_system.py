#!/usr/bin/env python3
"""
Test script to verify LPR System components
"""

import os
import sys
import cv2
import numpy as np
from dotenv import load_dotenv
from supabase_manager import SupabaseManager
from plate_detector import LicensePlateDetector

load_dotenv()

def test_tesseract():
    """Test if Tesseract OCR is properly installed"""
    try:
        import pytesseract
        # Test Tesseract availability
        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR is working")
        return True
    except Exception as e:
        print(f"❌ Tesseract OCR error: {e}")
        print("Please install Tesseract OCR and update .env file")
        return False

def test_opencv():
    """Test if OpenCV is properly installed"""
    try:
        # Test OpenCV by creating a simple image
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite('test_output.jpg', test_img)
        if os.path.exists('test_output.jpg'):
            os.remove('test_output.jpg')
            print("✅ OpenCV is working")
            return True
    except Exception as e:
        print(f"❌ OpenCV error: {e}")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or supabase_url == 'your_supabase_project_url':
            print("❌ Supabase URL not configured in .env")
            return False
        
        if not supabase_key or supabase_key == 'your_supabase_anon_key':
            print("❌ Supabase key not configured in .env")
            return False
        
        manager = SupabaseManager()
        if manager.test_connection():
            print("✅ Supabase connection is working")
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ Supabase connection error: {e}")
        return False

def test_plate_detector():
    """Test license plate detector"""
    try:
        detector = LicensePlateDetector()
        print("✅ License plate detector initialized")
        return True
    except Exception as e:
        print(f"❌ Plate detector error: {e}")
        return False

def create_test_image():
    """Create a simple test image with text"""
    # Create a blank white image
    img = np.ones((200, 400, 3), dtype=np.uint8) * 255
    
    # Add some text (simulating a license plate)
    text = "ABC123"
    cv2.putText(img, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    
    # Save test image
    cv2.imwrite('test_plate.jpg', img)
    print("📷 Created test image: test_plate.jpg")
    return 'test_plate.jpg'

def main():
    print("🔍 Testing LPR System Components...\n")
    
    tests = [
        ("OpenCV", test_opencv),
        ("Tesseract OCR", test_tesseract),
        ("Supabase Connection", test_supabase_connection),
        ("Plate Detector", test_plate_detector),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- Testing {test_name} ---")
        result = test_func()
        results.append(result)
    
    print(f"\n{'='*50}")
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("\n🎉 All components are working!")
        
        # Create test image for manual testing
        create_test_image()
        
        print("\n📋 Next Steps:")
        print("1. Test with a real image:")
        print("   python main.py --mode image --input test_plate.jpg")
        print("2. Or test with live camera:")
        print("   python main.py --mode camera")
        print("3. View records:")
        print("   python main.py --mode records")
        
    else:
        print("\n⚠️  Some components need attention.")
        print("Please fix the issues above before proceeding.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
