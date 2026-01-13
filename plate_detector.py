import cv2
import numpy as np
import pytesseract
import os
from dotenv import load_dotenv

load_dotenv()

# Set Tesseract path for Windows
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH', 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe')

class LicensePlateDetector:
    def __init__(self):
        # Load the cascade classifier for license plate detection
        try:
            self.plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_license_plate_rus_16stages.xml')
        except:
            print("Warning: License plate cascade not found. Using contour-based detection.")
            self.plate_cascade = None
    
    def preprocess_image(self, image):
        """Preprocess image for better plate detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter to preserve edges while reducing noise
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        
        # Apply edge detection
        edged = cv2.Canny(gray, 30, 200)
        
        return gray, edged
    
    def detect_plates_cascade(self, image):
        """Detect license plates using cascade classifier"""
        gray, _ = self.preprocess_image(image)
        
        if self.plate_cascade is None:
            return []
        
        plates = self.plate_cascade.detectMultiScale(gray, 1.1, 4)
        return plates
    
    def detect_plates_contours(self, image):
        """Detect license plates using contour detection"""
        gray, edged = self.preprocess_image(image)
        
        # Find contours
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours by area and keep the largest ones
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        plate_contours = []
        
        for contour in contours:
            # Approximate the contour
            approx = cv2.approxPolyDP(contour, 0.018 * cv2.arcLength(contour, True), True)
            
            # Look for rectangular shapes with 4 corners
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / h
                
                # License plates typically have aspect ratio between 2 and 6
                if 2 <= aspect_ratio <= 6:
                    plate_contours.append((x, y, w, h))
        
        return plate_contours
    
    def extract_plate_text(self, plate_image):
        """Extract text from license plate image using OCR"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get binary image
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Apply morphological operations to remove noise
            kernel = np.ones((3,3), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            
            # Configure Tesseract for license plate recognition
            custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            
            # Extract text
            text = pytesseract.image_to_string(thresh, config=custom_config)
            
            # Clean the text
            text = ''.join(c for c in text if c.isalnum()).upper()
            
            return text if len(text) >= 5 else ""  # Return only if reasonable plate length
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def detect_and_read_plates(self, image):
        """Main method to detect and read license plates from image"""
        detected_plates = []
        
        # Try cascade detection first
        if self.plate_cascade is not None:
            cascade_plates = self.detect_plates_cascade(image)
            for (x, y, w, h) in cascade_plates:
                plate_img = image[y:y+h, x:x+w]
                plate_text = self.extract_plate_text(plate_img)
                if plate_text:
                    detected_plates.append({
                        'text': plate_text,
                        'bbox': (x, y, w, h),
                        'image': plate_img
                    })
        
        # If no plates found with cascade, try contour detection
        if not detected_plates:
            contour_plates = self.detect_plates_contours(image)
            for (x, y, w, h) in contour_plates:
                plate_img = image[y:y+h, x:x+w]
                plate_text = self.extract_plate_text(plate_img)
                if plate_text:
                    detected_plates.append({
                        'text': plate_text,
                        'bbox': (x, y, w, h),
                        'image': plate_img
                    })
        
        return detected_plates
