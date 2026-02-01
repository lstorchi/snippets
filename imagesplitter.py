import os
import sys
import cv2
import numpy as np

def extract_photos_from_scan(image_path, 
                             min_area=5000,
                             startcount=1):
    # 1. Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image at {image_path}")
        return

    # 2. Resize for processing (Detection Phase)
    # We work on a smaller copy to avoid SegFaults and speed up detection
    # The final crop will still be from the original high-res image
    scale_percent = 30  # Downscale to 30% for detection
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    img_small = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    # 3. Preprocessing
    # Convert to grayscale
    gray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
    
    # Add a slight blur to remove scanner noise/dust
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. Thresholding
    # The background is white (high values). We invert it so the background becomes 
    # black (0) and the photos become white/foreground.
    # We use 230 as a cutoff to catch aged/yellowed photo paper against pure white background.
    _, thresh = cv2.threshold(blur, 230, 255, cv2.THRESH_BINARY_INV)

    # 5. Morphological Operations (Optional cleanup)
    # This closes small gaps inside the photos to make them solid blocks
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 6. Find Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Found {len(contours)} potential objects.")

    saved_count = 0
    for i, c in enumerate(contours):
        # Calculate area on the small image
        area = cv2.contourArea(c)
        
        # Filter out small noise (dots, dust lines)
        # Note: min_area is relative to the *scaled down* image
        if area > min_area:
            # 7. Get Bounding Box
            x, y, w, h = cv2.boundingRect(c)
            
            # 8. Map coordinates back to Original Image Size
            scale_factor = 100 / scale_percent
            x_orig = int(x * scale_factor)
            y_orig = int(y * scale_factor)
            w_orig = int(w * scale_factor)
            h_orig = int(h * scale_factor)

            # Ensure we don't go out of bounds (just in case)
            h_orig = min(h_orig, img.shape[0] - y_orig)
            w_orig = min(w_orig, img.shape[1] - x_orig)

            # 9. Crop from the ORIGINAL high-res image
            crop = img[y_orig:y_orig+h_orig, x_orig:x_orig+w_orig]
            
            # Save the file
            filename = f"foto{startcount + saved_count:04d}.jpg"
            cv2.imwrite(filename, crop)
            print(f"Saved {filename}")
            saved_count += 1

    print(f"Extraction complete. Saved {saved_count} photos.")

    return saved_count

# Run the function
# Adjust 'min_area' if it misses small photos or picks up dust

if len(sys.argv) != 3:
    print("Usage: ", sys.argv[0], " <images_path> <start_count>")
    sys.exit(1)

newcount = int(sys.argv[2])
for imagename in os.listdir(sys.argv[1]):
    image_path = os.path.join(sys.argv[1], imagename)
    howmany = extract_photos_from_scan(image_path, min_area=1000, \
                          startcount=newcount)
    newcount += howmany