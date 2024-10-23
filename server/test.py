import cv2
from skimage.feature import hog
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return img_bin

def extract_features(image):
    features, hog_image = hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)
    return features

# Assuming X contains your features and y contains the corresponding labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create SVM classifier
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

# Test the classifier
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

def predict_character(image_path, model):
    img = preprocess_image(image_path)
    features = extract_features(img)
    return model.predict([features])[0]
