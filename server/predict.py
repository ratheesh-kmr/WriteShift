import joblib
import cv2
from skimage.feature import hog
import os

image_path = '/home/krish/Desktop/Programming/ml/sem-project/WriteShift/server/pic.jpg'
print("Absolute path:", os.path.abspath(image_path))

# Load the saved model
model_path = 'handwriting_recognition_model.pkl'
clf = joblib.load(model_path)
print(f"Model loaded from {model_path}")

# Preprocess and extract features from the input image
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return img_bin

def extract_features(image):
    # Use the same parameters as during training
    features, hog_image = hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)
    return features.flatten()  # Flatten the features to ensure a 1D array

# Predict text from a new image
def predict_text(image_path):
    img = preprocess_image(image_path)
    
    # Check if the image is loaded correctly and is of sufficient size
    if img is None or img.shape[0] < 16 or img.shape[1] < 16:
        raise ValueError("Input image is too small for HOG feature extraction. It should be at least 16x16 pixels.")
    
    features = extract_features(img)
    
    print(f"Features size: {features.shape}")  # Print feature size for debugging
    prediction = clf.predict([features])[0]
    return prediction

# Example of usage
predicted_text = predict_text(image_path)
print(f"Predicted text: {predicted_text}")
