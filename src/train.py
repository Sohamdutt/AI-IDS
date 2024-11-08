# train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Import the preprocessing function from preprocess.py
from preprocess import preprocess_data

def load_preprocessed_data(file_path):
    """
    Load and preprocess the data for training.
    
    Args:
        file_path (str): Path to the data file.
        
    Returns:
        X, y (pd.DataFrame, pd.Series): Features and labels for training.
    """
    df = preprocess_data(file_path)
    X = df.drop('label', axis=1)  # Assuming 'label' is the target column
    y = df['label']
    return X, y

def train_model(X, y):
    """
    Train a machine learning model on the given data.
    
    Args:
        X (pd.DataFrame): Training features.
        y (pd.Series): Target labels.
        
    Returns:
        model (sklearn model): Trained machine learning model.
    """
    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Model Accuracy:", accuracy)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    return model

def save_model(model, model_path='model.pkl'):
    """
    Save the trained model to a file for future use.
    
    Args:
        model (sklearn model): Trained model to save.
        model_path (str): File path for saving the model.
    """
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved to {model_path}")

def main():
    # Load and preprocess the data
    file_path = 'combine.csv'  # Path to your preprocessed network traffic data
    X, y = load_preprocessed_data(file_path)

    # Train the model
    model = train_model(X, y)

    # Save the trained model
    save_model(model, 'models/IDS_model.pkl')

if __name__ == '__main__':
    main()
