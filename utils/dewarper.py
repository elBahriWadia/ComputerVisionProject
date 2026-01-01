import cv2
import numpy as np
import os


def remove_white_background(image):
    """
    Remove white background from the processed image
    
    Args:
        image (numpy.ndarray): Input image
    
    Returns:
        numpy.ndarray: Image with white background removed
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to create a binary mask of non-white areas
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Apply the mask to the original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result


def order_points(pts):
    """
    Order points in top-left, top-right, bottom-right, bottom-left order
    
    Args:
        pts (numpy.ndarray): Array of 4 points
    
    Returns:
        numpy.ndarray: Ordered points
    """
    rect = np.zeros((4, 2), dtype="float32")
    
    # Top-left point will have the smallest sum
    # Bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # Top-right point will have the smallest difference
    # Bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect


def four_point_transform(image, pts):
    """
    Apply perspective transform to get bird's eye view of document
    
    Args:
        image (numpy.ndarray): Input image
        pts (numpy.ndarray): Source points
    
    Returns:
        numpy.ndarray: Transformed image with straight borders
    """
    # Obtain a consistent order of the points
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    # Compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    # Compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    # Construct destination points for straight borders
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")
    
    # Compute the perspective transform matrix and apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped


def dewarp_document(image_path, output_path):
    """
    Process document: remove white background and dewarp to straight borders
    
    Args:
        image_path (str): Path to input image
        output_path (str): Path to save dewarped image
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            return False
        
        # Remove white background
        no_bg_image = remove_white_background(image)
        
        # Convert to grayscale for contour detection
        gray = cv2.cvtColor(no_bg_image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(
            gray, 
            0, 
            255, 
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        
        # Find contours
        contours, _ = cv2.findContours(
            thresh, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            print("No contours found for dewarping")
            return False
        
        # Find the largest contour (document)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get the minimum area rectangle for perspective correction
        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = box.astype(np.int32)
        
        # Apply perspective transform to straighten borders
        try:
            dewarped = four_point_transform(
                no_bg_image, 
                box.reshape(4, 2).astype(np.float32)
            )
        except Exception as e:
            print(f"Error applying perspective transform: {e}")
            # If dewarping fails, save the image without background removal
            dewarped = no_bg_image
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the dewarped image
        cv2.imwrite(output_path, dewarped)
        
        print(f"Document dewarped and saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error in dewarping: {str(e)}")
        return False


def crop_to_content(image):
    """
    Crop image to remove excess white space around content
    
    Args:
        image (numpy.ndarray): Input image
    
    Returns:
        numpy.ndarray: Cropped image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold
    _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(
        thresh, 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    if not contours:
        return image
    
    # Get bounding rectangle of all content
    x, y, w, h = cv2.boundingRect(np.vstack(contours))
    
    # Add small padding
    padding = 10
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(image.shape[1] - x, w + 2 * padding)
    h = min(image.shape[0] - y, h + 2 * padding)
    
    # Crop
    cropped = image[y:y+h, x:x+w]
    
    return cropped


def enhance_document(image_path, output_path):
    """
    Additional enhancement: increase contrast and sharpness
    
    Args:
        image_path (str): Path to input image
        output_path (str): Path to save enhanced image
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False
        
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Sharpen
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)
        
        cv2.imwrite(output_path, enhanced)
        return True
        
    except Exception as e:
        print(f"Error enhancing document: {str(e)}")
        return False
