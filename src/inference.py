# inference.py
import pickle
import pandas as pd
import numpy as np

# Load the preprocess_data function from preprocess.py for any required preprocessing steps
from preprocess import preprocess_single_record

# Path to the trained model file
MODEL_PATH = 'IDS_model.pkl'

def load_model(model_path=MODEL_PATH):
    """
    Load the trained machine learning model from a file.
    
    Args:
        model_path (str): Path to the saved model file.
        
    Returns:
        model (sklearn model): Loaded machine learning model.
    """
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    print("Model loaded successfully.")
    return model

def make_prediction(model, data):
    """
    Make a prediction on new data using the loaded model.
    
    Args:
        model (sklearn model): The loaded machine learning model.
        data (pd.DataFrame or dict): The data to predict on (single record).
        
    Returns:
        prediction (str): The predicted class (e.g., "normal" or "threat").
    """
    # Preprocess the incoming data record if necessary
    processed_data = preprocess_single_record(data)
    
    # Convert to DataFrame format expected by the model
    data_df = pd.DataFrame([processed_data])
    
    # Make a prediction
    prediction = model.predict(data_df)
    prediction_proba = model.predict_proba(data_df)
    
    return prediction[0], prediction_proba[0]

def main():
    # Load the trained model
    model = load_model()

    # Example input data (replace this with real-time network data)
    example_data = {
        'src_ip': '192.168.1.1',
        'dest_ip': '192.168.1.2',
        'src_port': 12345,
        'dest_port': 80,
        'protocol': 6,
        'packet_size': 512,
        # add other features as required by your model
    }
    
    # Make a prediction on the example data
    prediction, prediction_proba = make_prediction(model, example_data)
    print(f"Prediction: {prediction}, Probability: {prediction_proba}")

if __name__ == '__main__':
    main()
