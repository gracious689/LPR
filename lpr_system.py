import cv2
import os
import time
from datetime import datetime
from plate_detector import LicensePlateDetector
from supabase_manager import SupabaseManager

class LPRSystem:
    def __init__(self, camera_location="Main Entrance"):
        self.detector = LicensePlateDetector()
        self.db_manager = SupabaseManager()
        self.camera_location = camera_location
        self.processed_plates = set()  # To avoid duplicate processing
        self.last_processed_time = {}
        
    def process_image_file(self, image_path):
        """Process a single image file for license plates"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not read image {image_path}")
                return []
            
            # Detect and read plates
            detected_plates = self.detector.detect_and_read_plates(image)
            
            results = []
            for plate in detected_plates:
                plate_text = plate['text']
                
                # Check if we've recently processed this plate (avoid duplicates)
                current_time = time.time()
                if plate_text in self.last_processed_time:
                    if current_time - self.last_processed_time[plate_text] < 30:  # 30 second cooldown
                        continue
                
                # Store in database
                record_id = self.db_manager.insert_plate_record(
                    plate_number=plate_text,
                    confidence_score=0.8,  # Placeholder confidence score
                    image_path=image_path,
                    camera_location=self.camera_location
                )
                
                if record_id:
                    self.last_processed_time[plate_text] = current_time
                    results.append({
                        'plate_number': plate_text,
                        'timestamp': datetime.now(),
                        'record_id': record_id,
                        'bbox': plate['bbox']
                    })
                    
                    print(f"✓ Detected and stored: {plate_text}")
            
            return results
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return []
    
    def process_video_stream(self, camera_index=0, save_frames=False):
        """Process live video stream from camera"""
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return
        
        print("Starting live LPR detection. Press 'q' to quit.")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            frame_count += 1
            
            # Process every 10th frame to reduce computational load
            if frame_count % 10 == 0:
                detected_plates = self.detector.detect_and_read_plates(frame)
                
                for plate in detected_plates:
                    plate_text = plate['text']
                    x, y, w, h = plate['bbox']
                    
                    # Check for recent duplicates
                    current_time = time.time()
                    if plate_text in self.last_processed_time:
                        if current_time - self.last_processed_time[plate_text] < 30:
                            continue
                    
                    # Store in database
                    record_id = self.db_manager.insert_plate_record(
                        plate_number=plate_text,
                        confidence_score=0.8,
                        image_path=None,  # Live stream, no saved image path
                        camera_location=self.camera_location
                    )
                    
                    if record_id:
                        self.last_processed_time[plate_text] = current_time
                        
                        # Draw bounding box and text on frame
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, plate_text, (x, y - 10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        
                        print(f"✓ Live detection: {plate_text}")
            
            # Display the frame
            cv2.imshow('LPR System - Live Detection', frame)
            
            # Save frame if requested
            if save_frames and frame_count % 100 == 0:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(f"frames/frame_{timestamp}.jpg", frame)
            
            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def process_image_folder(self, folder_path):
        """Process all images in a folder"""
        if not os.path.exists(folder_path):
            print(f"Error: Folder {folder_path} does not exist")
            return
        
        # Supported image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        # Get all image files
        image_files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(folder_path, file))
        
        print(f"Found {len(image_files)} images to process")
        
        total_plates = 0
        for image_file in image_files:
            print(f"Processing: {image_file}")
            plates = self.process_image_file(image_file)
            total_plates += len(plates)
        
        print(f"Processing complete. Total plates detected: {total_plates}")
    
    def show_recent_records(self, limit=10):
        """Display recent license plate records"""
        records = self.db_manager.get_plate_records(limit)
        
        if not records:
            print("No records found")
            return
        
        print("\nRecent License Plate Records:")
        print("-" * 80)
        for record in records:
            print(f"ID: {record['id']} | Plate: {record['plate_number']} | "
                  f"Time: {record['timestamp']} | Location: {record['camera_location']}")
    
    def cleanup(self):
        """Clean up resources"""
        if self.db_manager:
            self.db_manager.close()
