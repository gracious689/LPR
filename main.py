#!/usr/bin/env python3
"""
License Plate Recognition (LPR) System
Main entry point for the LPR application
"""

import os
import sys
import argparse
from lpr_system import LPRSystem
from supabase_setup import create_supabase_table

def main():
    parser = argparse.ArgumentParser(description='License Plate Recognition System')
    parser.add_argument('--mode', choices=['setup', 'image', 'folder', 'camera', 'records'], 
                       required=True, help='Operation mode')
    parser.add_argument('--input', help='Input file/folder path (for image/folder modes)')
    parser.add_argument('--camera', type=int, default=0, help='Camera index (for camera mode)')
    parser.add_argument('--location', default='Main Entrance', help='Camera location identifier')
    parser.add_argument('--limit', type=int, default=10, help='Limit for records display')
    
    args = parser.parse_args()
    
    # Initialize LPR system
    lpr_system = LPRSystem(camera_location=args.location)
    
    try:
        if args.mode == 'setup':
            print("Setting up Supabase database...")
            if create_supabase_table():
                print("✓ Supabase setup completed successfully")
            else:
                print("✗ Supabase setup failed")
                sys.exit(1)
        
        elif args.mode == 'image':
            if not args.input:
                print("Error: --input path required for image mode")
                sys.exit(1)
            
            if not os.path.exists(args.input):
                print(f"Error: Image file {args.input} not found")
                sys.exit(1)
            
            print(f"Processing image: {args.input}")
            results = lpr_system.process_image_file(args.input)
            
            if results:
                print(f"\nDetected {len(results)} license plate(s):")
                for result in results:
                    print(f"  - {result['plate_number']} at {result['timestamp']}")
            else:
                print("No license plates detected")
        
        elif args.mode == 'folder':
            if not args.input:
                print("Error: --input path required for folder mode")
                sys.exit(1)
            
            lpr_system.process_image_folder(args.input)
        
        elif args.mode == 'camera':
            print("Starting live camera detection...")
            print("Press 'q' to quit the camera view")
            lpr_system.process_video_stream(camera_index=args.camera)
        
        elif args.mode == 'records':
            lpr_system.show_recent_records(limit=args.limit)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        lpr_system.cleanup()

if __name__ == "__main__":
    main()
