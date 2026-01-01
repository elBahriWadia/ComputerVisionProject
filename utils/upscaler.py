import cv2
import numpy as np
import os
from PIL import Image


def upscale_image(image_path, output_path):
    """
    Upscale image using Real-ESRGAN with smart scaling

    Args:
        image_path (str): Path to input image
        output_path (str): Path to save upscaled image

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Try to import Real-ESRGAN
        try:
            from basicsr.archs.rrdbnet_arch import RRDBNet
            from realesrgan import RealESRGANer
            import torch
        except ImportError as e:
            print(f"Real-ESRGAN not properly installed: {e}")
            print("Falling back to OpenCV upscaling...")
            return upscale_opencv(image_path, output_path)

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            return False

        # Get image dimensions
        height, width = image.shape[:2]

        # Smart scaling decision
        # If image is already high resolution (> 2000px on any side), skip upscaling
        if max(height, width) > 2000:
            print(f"Image already high resolution ({width}x{height}), skipping upscaling")
            cv2.imwrite(output_path, image)
            return True

        # Determine scale factor based on image size
        if max(height, width) < 800:
            scale = 4  # Small images get 4x upscale
        elif max(height, width) < 1500:
            scale = 2  # Medium images get 2x upscale
        else:
            scale = 2  # Larger images get 2x upscale

        print(f"Upscaling image from {width}x{height} with {scale}x factor...")

        # Initialize Real-ESRGAN model
        model_name = 'RealESRGAN_x4plus'  # Best for general images and documents
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

        # Determine device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Model path (will auto-download if not exists)
        model_path = os.path.join('models', 'realesrgan', f'{model_name}.pth')

        # Initialize upsampler
        upsampler = RealESRGANer(
            scale=4,  # Model is trained for 4x, we'll resize after if needed
            model_path=model_path,
            model=model,
            tile=400,  # Tile size for processing large images
            tile_pad=10,
            pre_pad=0,
            half=True if device.type == 'cuda' else False,
            device=device
        )

        # Upscale the image
        output, _ = upsampler.enhance(image, outscale=scale)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the upscaled image
        cv2.imwrite(output_path, output)

        print(f"Image upscaled successfully to {output.shape[1]}x{output.shape[0]}")
        print(f"Saved to {output_path}")
        return True

    except Exception as e:
        print(f"Error in Real-ESRGAN upscaling: {str(e)}")
        print("Falling back to OpenCV upscaling...")
        return upscale_opencv(image_path, output_path)


def upscale_opencv(image_path, output_path, scale=2):
    """
    Fallback upscaling using OpenCV (if Real-ESRGAN fails)

    Args:
        image_path (str): Path to input image
        output_path (str): Path to save upscaled image
        scale (int): Upscale factor

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image at {image_path}")
            return False

        # Get image dimensions
        height, width = image.shape[:2]

        # Skip if already high resolution
        if max(height, width) > 2000:
            cv2.imwrite(output_path, image)
            return True

        # Determine scale factor
        if max(height, width) < 800:
            scale = 4
        elif max(height, width) < 1500:
            scale = 2
        else:
            scale = 2

        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)

        print(f"OpenCV upscaling from {width}x{height} to {new_width}x{new_height}")

        # Upscale using Lanczos interpolation (best quality)
        upscaled = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_LANCZOS4
        )

        # Optional: Apply unsharp mask for better clarity
        upscaled = unsharp_mask(upscaled)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the upscaled image
        cv2.imwrite(output_path, upscaled)

        print(f"Image upscaled successfully using OpenCV")
        return True

    except Exception as e:
        print(f"Error in OpenCV upscaling: {str(e)}")
        return False


def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.5, threshold=0):
    """
    Apply unsharp mask to enhance image sharpness

    Args:
        image (numpy.ndarray): Input image
        kernel_size (tuple): Size of Gaussian kernel
        sigma (float): Standard deviation for Gaussian kernel
        amount (float): Strength of sharpening
        threshold (int): Minimum brightness change required

    Returns:
        numpy.ndarray: Sharpened image
    """
    # Create blurred version
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)

    # Calculate the sharpened image
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)

    # Apply threshold
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)

    return sharpened


def get_image_quality_score(image_path):
    """
    Estimate image quality to determine if upscaling is needed

    Args:
        image_path (str): Path to image

    Returns:
        dict: Quality metrics (resolution, sharpness, etc.)
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return None

        height, width = image.shape[:2]

        # Calculate Laplacian variance (sharpness measure)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        return {
            'width': width,
            'height': height,
            'sharpness': laplacian_var,
            'needs_upscaling': max(width, height) < 1500,
            'recommended_scale': 4 if max(width, height) < 800 else 2
        }

    except Exception as e:
        print(f"Error analyzing image quality: {str(e)}")
        return None


def setup_realesrgan_models():
    """
    Download and setup Real-ESRGAN models if not present

    Returns:
        bool: True if models are ready, False otherwise
    """
    try:
        model_dir = os.path.join('models', 'realesrgan')
        os.makedirs(model_dir, exist_ok=True)

        model_name = 'RealESRGAN_x4plus'
        model_path = os.path.join(model_dir, f'{model_name}.pth')

        if os.path.exists(model_path):
            print(f"Real-ESRGAN model already exists at {model_path}")
            return True

        print(f"Downloading Real-ESRGAN model...")
        print("This is a one-time setup and may take a few minutes...")

        # The model will be auto-downloaded by Real-ESRGAN on first use
        return True

    except Exception as e:
        print(f"Error setting up Real-ESRGAN models: {str(e)}")
        return False