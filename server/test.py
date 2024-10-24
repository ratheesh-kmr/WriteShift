import os
import cv2
import pandas as pd
import numpy as np
import joblib
from sklearn.svm import SVC
from skimage.feature import hog

# Preprocessing function
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Failed to load image: {image_path}")
        return None
    _, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return img_bin

# Feature extraction
def extract_features(image):
    features, hog_image = hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)
    return features

# Load the dataset using CSV file for labels
def load_dataset(dataset_path, csv_file):
    data = pd.read_csv(csv_file)
    X = []
    y = []
    
    # Use a set for expected feature length
    expected_feature_length = None
    
    for idx, row in data.iterrows():
        image_file = row['FILENAME']
        label = row['IDENTITY']
        image_path = os.path.join(dataset_path, image_file)
        
        if image_file > 'TRAIN_01000.jpg':
            print("Reached TRAIN_01000.jpg, stopping dataset loading.")
            break
        
        if os.path.exists(image_path):
            print(f"Processing file: {image_path}")
            img = preprocess_image(image_path)
            if img is not None and img.shape[0] >= 16 and img.shape[1] >= 16:  # Minimum size check
                features = extract_features(img)
                
                # Check if feature length is consistent
                if expected_feature_length is None:
                    expected_feature_length = len(features)  # Set expected length from the first valid feature vector
                
                if len(features) == expected_feature_length:  # Only append if lengths match
                    X.append(features)
                    y.append(label)
                else:
                    print(f"Feature length mismatch for {image_file}: expected {expected_feature_length}, got {len(features)}")
            else:
                print(f"Image {image_file} is either too small or failed to load.")
        else:
            print(f"Image {image_file} not found in {dataset_path}.")
    
    print(f"Loaded {len(X)} images and {len(y)} labels.")
    
    if len(X) == 0 or len(y) == 0:
        print("No valid images found.")
        return np.array([]), np.array([])  # Handle empty cases
    
    return np.array(X), np.array(y)  # Convert to NumPy arrays

# Example paths
train_csv = '/home/krish/Desktop/Programming/ml/sem-project/WriteShift/server/dataset/written_name_train_v2.csv'
train_images_path = '/home/krish/Desktop/Programming/ml/sem-project/WriteShift/server/dataset/train_v2/train'

# Load the dataset
X, y = load_dataset(train_images_path, train_csv)

# Train the model
clf = SVC()  # or any other classifier
clf.fit(X, y)

# Save the model
model_path = 'handwriting_recognition_model.pkl'
joblib.dump(clf, model_path)
print(f"Model saved to {model_path}")
