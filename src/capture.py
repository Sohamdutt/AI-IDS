# capture.py
from scapy.all import sniff
import pandas as pd
from datetime import datetime
from inference import make_prediction, load_model
import json

# Load the trained model
model = load_model()

def packet_to_dict(packet):
    """
    Extract relevant features from a network packet.
    
    Args:
        packet: Scapy packet object.
        
    Returns:
        dict: Dictionary of extracted packet features.
    """
    try:
        packet_data = {
            'src_ip': packet[0][1].src,
            'dest_ip': packet[0][1].dst,
            'src_port': packet[0][2].sport if hasattr(packet[0][2], 'sport') else None,
            'dest_port': packet[0][2].dport if hasattr(packet[0][2], 'dport') else None,
            'protocol': packet[0][1].proto,
            'packet_size': len(packet)
            # Add other features as needed
        }
        return packet_data
    except IndexError:
        return None

def process_packet(packet):
    """
    Callback function for each captured packet.
    
    Args:
        packet: Scapy packet object.
    """
    packet_data = packet_to_dict(packet)
    if packet_data:
        # Make a prediction using the IDS model
        prediction, probability = make_prediction(model, packet_data)
        
        # Log the prediction
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Prediction: {prediction}, Probability: {probability}")
        
        # Save the alert to a log file if it is a threat
        if prediction == "threat":
            with open("alerts.log", "a") as alert_log:
                alert_log.write(json.dumps({
                    'timestamp': timestamp,
                    'src_ip': packet_data['src_ip'],
                    'dest_ip': packet_data['dest_ip'],
                    'prediction': prediction,
                    'probability': probability.tolist()
                }) + "\n")

def start_sniffing(interface="eth0", packet_count=0):
    """
    Start capturing packets in real-time.
    
    Args:
        interface (str): Network interface to listen on.
        packet_count (int): Number of packets to capture (0 for infinite).
    """
    print(f"Starting packet capture on interface {interface}...")
    sniff(iface=interface, prn=process_packet, count=packet_count, store=False)

if __name__ == "__main__":
    # Start capturing packets on the specified interface (e.g., "eth0" or "wlan0")
    start_sniffing(interface="eth0", packet_count=0)
