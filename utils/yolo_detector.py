import cv2
import numpy as np
import torch
from ultralytics import YOLO
import os


def detect_and_extract_document(image_path, model_path, output_path):
    """
    Detect document using YOLO and extract it with mask processing
    
    Args:
        image_path (str): Path to input image
        model_path (str): Path to trained YOLO model
        output_path (str): Path to save extracted document
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if model exists
        if not os.path.exists(model_path):
            print(f"Error: Model not found at {model_path}")
            return False
        
        # Load the YOLO model
        model = YOLO(model_path)
        
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            return False
        
        # Run inference
        results = model(image)[0]
        
        # Check if masks were detected
        if results.masks is None or len(results.masks.data) == 0:
            print("No document detected in image")
            return False
        
        # Get the first mask (assuming single document detection)
        mask = results.masks.data[0].cpu().numpy()
        
        # Convert mask to binary image
        binary_mask = (mask > 0.5).astype(np.uint8) * 255
        
        # Resize mask to original image size if needed
        if binary_mask.shape[:2] != image.shape[:2]:
            binary_mask = cv2.resize(
                binary_mask, 
                (image.shape[1], image.shape[0]),
                interpolation=cv2.INTER_NEAREST
            )
        
        # Find contours
        contours, _ = cv2.findContours(
            binary_mask, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            print("No contours found in mask")
            return False
        
        # Find the largest contour (main document)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Create a blank mask and fill the largest contour
        filled_mask = np.zeros_like(binary_mask)
        cv2.drawContours(filled_mask, [largest_contour], -1, 255, -1)
        
        # Morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        filled_mask = cv2.morphologyEx(
            filled_mask, 
            cv2.MORPH_CLOSE, 
            kernel, 
            iterations=2
        )
        
        # Create a binary mask for extraction
        filled_mask_binary = (filled_mask > 0).astype(np.uint8)
        
        # Extract document using the mask
        extracted_document = cv2.bitwise_and(
            image, 
            image, 
            mask=filled_mask_binary
        )
        
        # Create a white background
        white_background = np.ones_like(image) * 255
        
        # Replace black regions with white
        result = np.where(
            filled_mask_binary[:, :, np.newaxis] == 1,
            extracted_document,
            white_background
        )
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the extracted document
        cv2.imwrite(output_path, result)
        
        print(f"Document extracted and saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error in document detection: {str(e)}")
        return False


def get_document_bounds(image_path, model_path):
    """
    Get the bounding coordinates of the detected document
    
    Args:
        image_path (str): Path to input image
        model_path (str): Path to trained YOLO model
    
    Returns:
        tuple: (x, y, w, h) bounding box coordinates or None if failed
    """
    try:
        model = YOLO(model_path)
        image = cv2.imread(image_path)
        
        if image is None:
            return None
        
        results = model(image)[0]
        
        if results.masks is None or len(results.masks.data) == 0:
            return None
        
        mask = results.masks.data[0].cpu().numpy()
        binary_mask = (mask > 0.5).astype(np.uint8) * 255
        
        if binary_mask.shape[:2] != image.shape[:2]:
            binary_mask = cv2.resize(
                binary_mask,
                (image.shape[1], image.shape[0]),
                interpolation=cv2.INTER_NEAREST
            )
        
        contours, _ = cv2.findContours(
            binary_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            return None
        
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        return (x, y, w, h)
        
    except Exception as e:
        print(f"Error getting document bounds: {str(e)}")
        return None
