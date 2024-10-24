import os
import numpy as np
from flask import Flask, request, jsonify
import cv2
from skimage.feature import hog
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Path to the dataset
dataset_path = r"C:\Users\rathe\Documents\Ratheesh got bored\SEMESTER 5\Project\Dataset\archive"

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

# Load the dataset from the folder
def load_dataset(dataset_path):
    X = []
    y = []
    
    # Check the dataset path to see if it exists
    if not os.path.exists(dataset_path):
        print(f"Dataset path does not exist: {dataset_path}")
        return np.array(X), np.array(y)

    # List all labels (subdirectories)
    for label in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, label)
        print(f"Checking: {folder_path}")
        
        # Check if the path is a directory and not a file
        if os.path.isdir(folder_path):
            print(f"Loading images from: {folder_path}")
            files = os.listdir(folder_path)  # List all files in the directory
            
            if not files:
                print(f"No files found in directory: {folder_path}")
                continue
            
            for image_file in files:
                image_path = os.path.join(folder_path, image_file)
                print(f"Processing file: {image_path}")
                
                # Validate if the file is an image based on its extension
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  
                    img = preprocess_image(image_path)
                    if img is not None and img.shape[0] >= 16 and img.shape[1] >= 16:  # Minimum size check
                        features = extract_features(img)
                        X.append(features)
                        y.append(label)  # Assuming the folder name is the label
                        print(f"Loaded image: {image_file}")
                    else:
                        print(f"Image {image_file} is either too small or failed to load.")
                else:
                    print(f"File {image_file} is not a valid image.")
        else:
            print(f"'{label}' is not a directory, skipping it.")

    print(f"Loaded {len(X)} images and {len(y)} labels.")
    return np.array(X), np.array(y)  # Convert to NumPy arrays




# Load dataset
X, y = load_dataset(dataset_path)
print(f"Loaded {len(X)} images and {len(y)} labels.")

if len(X) == 0 or len(y) == 0:
    print("No images loaded. Please check your dataset path and structure.")
else:
    # Splitting dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train SVM model
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)

    # Testing the classifier
    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))

@app.route('/predict', methods=['POST'])
def predict_character():
    image_file = request.files['image']
    image_path = './temp_image.png'
    image_file.save(image_path)
    
    # Preprocess and predict
    img = preprocess_image(image_path)
    if img is not None:
        features = extract_features(img)
        prediction = clf.predict([features])[0]
        return jsonify({'character': prediction})
    else:
        return jsonify({'error': 'Failed to process the image'}), 400

if __name__ == '__main__':
    app.run(debug=True)
