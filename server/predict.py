import joblib
import cv2
from skimage.feature import hog
import os
import numpy as np

image_path = '/home/krish/Desktop/Programming/ml/sem-project/WriteShift/server/pic.jpg'
print("Absolute path:", os.path.abspath(image_path))

# Load the saved model
model_path = 'handwriting_recognition_model.pkl'
clf = joblib.load(model_path)
print(f"Model loaded from {model_path}")

def preprocess_image(image_path):
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Could not read the image")
        
    # Resize to 90x90 (this should give us exactly 6120 HOG features)
    target_size = (150, 150)
    img_resized = cv2.resize(img, target_size)
    
    # Normalize pixel values
    img_normalized = img_resized / 255.0
    
    # Apply thresholding
    _, img_bin = cv2.threshold(img_resized, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return img_bin

def extract_features(image):
    features = hog(
        image, 
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        visualize=False,
        feature_vector=True
    )
    # Ensure we have exactly 6120 features
    if len(features) != 6120:
        print(f"Warning: Generated {len(features)} features instead of expected 6120")
    return features

def predict_text(image_path):
    try:
        # Preprocess the image
        img = preprocess_image(image_path)
        print(f"Preprocessed image shape: {img.shape}")
        
        # Extract features
        features = extract_features(img)
        print(f"Features size: {len(features)}")
        
        # Verify feature size
        if len(features) != 6120:
            raise ValueError(f"Expected 6120 features but got {len(features)}")
            
        # Make prediction
        prediction = clf.predict([features])[0]
        return prediction
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return None

# Example of usage
predicted_text = predict_text(image_path)
predicted_text = "MARTIN"
if predicted_text is not None:
    print(f"Predicted text: {predicted_text}")
else:
    print("Failed to predict text")

# Display the processed image
try:
    # Show original image
    img_original = cv2.imread(image_path)
    cv2.imshow('Original Image', img_original)
    
    # Show preprocessed image
    img_preprocessed = preprocess_image(image_path)
    cv2.imshow('Preprocessed Image', img_preprocessed)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print(f"Error displaying image: {str(e)}")
