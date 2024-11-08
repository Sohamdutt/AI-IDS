# preprocess.py
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_data(file_path):
    """
    Load network traffic data from a CSV file or other sources.
    
    Args:
        file_path (str): Path to the data file.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    data = pd.read_csv(file_path)
    return data

def clean_data(df):
    """
    Clean the dataset by handling missing values and dropping irrelevant columns.
    
    Args:
        df (pd.DataFrame): The raw data.
        
    Returns:
        pd.DataFrame: Cleaned data.
    """
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Fill or drop missing values
    df = df.dropna()  # or use df.fillna(method='ffill') for forward fill

    # Drop irrelevant columns (e.g., timestamp if not used in feature extraction)
    if 'timestamp' in df.columns:
        df = df.drop(columns=['timestamp'])
    
    return df

def feature_extraction(df):
    """
    Extract relevant features such as packet size, protocol type, etc.
    
    Args:
        df (pd.DataFrame): Cleaned data.
        
    Returns:
        pd.DataFrame: Data with extracted features.
    """
    # Example feature: Protocol type encoding
    if 'protocol' in df.columns:
        protocol_encoder = LabelEncoder()
        df['protocol'] = protocol_encoder.fit_transform(df['protocol'])
    
    # Other feature engineering as required for IDS
    # e.g., Extracting source and destination port ranges, packet sizes, etc.
    
    return df

def normalize_features(df):
    """
    Normalize numerical features to a standard range for better model performance.
    
    Args:
        df (pd.DataFrame): Data with extracted features.
        
    Returns:
        pd.DataFrame: Normalized data.
    """
    # Selecting numerical columns for normalization
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    return df

def preprocess_data(file_path):
    """
    Complete preprocessing pipeline from loading data to final processed output.
    
    Args:
        file_path (str): Path to the data file.
        
    Returns:
        pd.DataFrame: Fully processed data ready for model training or inference.
    """
    # Step-by-step processing
    df = load_data(file_path)
    df = clean_data(df)
    df = feature_extraction(df)
    df = normalize_features(df)
    
    return df
