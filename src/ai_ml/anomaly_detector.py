import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import logging
from datetime import datetime, timedelta
import joblib

class AnomalyDetector:
    """
    Anomaly detection system for identifying unusual patterns in cybersecurity data.
    Uses multiple algorithms for comprehensive anomaly detection.
    """
    
    def __init__(self, method='isolation_forest', contamination=0.1):
        """
        Initialize the anomaly detector.
        
        Args:
            method (str): Detection method ('isolation_forest', 'dbscan', 'statistical')
            contamination (float): Expected proportion of anomalies
        """
        self.method = method
        self.contamination = contamination
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.baseline_stats = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize model based on method
        if method == 'isolation_forest':
            self.model = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=100
            )
        elif method == 'dbscan':
            self.model = DBSCAN(eps=0.5, min_samples=5)
        elif method == 'statistical':
            # Statistical method doesn't need a model object
            pass
        else:
            raise ValueError(f"Unsupported method: {method}")
    
    def extract_behavioral_features(self, user_data):
        """
        Extract behavioral features from user activity data.
        
        Args:
            user_data (dict): User activity data
            
        Returns:
            np.array: Feature vector
        """
        features = []
        
        # Login patterns
        login_times = user_data.get('login_times', [])
        if login_times:
            # Convert to hours of day
            hours = [datetime.fromisoformat(t.replace('Z', '+00:00')).hour for t in login_times]
            features.extend([
                np.mean(hours),  # Average login hour
                np.std(hours),   # Standard deviation of login hours
                len(set(hours)), # Number of unique login hours
                len(login_times) # Total login count
            ])
        else:
            features.extend([0, 0, 0, 0])
        
        # Access patterns
        features.extend([
            user_data.get('files_accessed', 0),
            user_data.get('applications_used', 0),
            user_data.get('data_downloaded_mb', 0),
            user_data.get('data_uploaded_mb', 0),
            user_data.get('failed_access_attempts', 0)
        ])
        
        # Network behavior
        features.extend([
            user_data.get('unique_ips_accessed', 0),
            user_data.get('external_connections', 0),
            user_data.get('suspicious_domains_accessed', 0),
            user_data.get('bandwidth_usage_mb', 0)
        ])
        
        # Time-based features
        session_durations = user_data.get('session_durations', [])
        if session_durations:
            features.extend([
                np.mean(session_durations),
                np.std(session_durations),
                max(session_durations),
                min(session_durations)
            ])
        else:
            features.extend([0, 0, 0, 0])
        
        return np.array(features).reshape(1, -1)
    
    def extract_network_features(self, network_data):
        """
        Extract features from network traffic data.
        
        Args:
            network_data (dict): Network traffic data
            
        Returns:
            np.array: Feature vector
        """
        features = []
        
        # Traffic volume
        features.extend([
            network_data.get('bytes_in', 0),
            network_data.get('bytes_out', 0),
            network_data.get('packets_in', 0),
            network_data.get('packets_out', 0)
        ])
        
        # Connection patterns
        features.extend([
            network_data.get('tcp_connections', 0),
            network_data.get('udp_connections', 0),
            network_data.get('failed_connections', 0),
            network_data.get('unique_destinations', 0)
        ])
        
        # Protocol distribution
        protocols = network_data.get('protocol_distribution', {})
        features.extend([
            protocols.get('http', 0),
            protocols.get('https', 0),
            protocols.get('ftp', 0),
            protocols.get('ssh', 0),
            protocols.get('dns', 0)
        ])
        
        # Timing features
        features.extend([
            network_data.get('avg_connection_duration', 0),
            network_data.get('peak_bandwidth_mbps', 0),
            network_data.get('connection_frequency', 0)
        ])
        
        return np.array(features).reshape(1, -1)
    
    def train_baseline(self, training_data, data_type='user_behavior'):
        """
        Train the anomaly detection model on baseline data.
        
        Args:
            training_data (list): List of normal behavior samples
            data_type (str): Type of data ('user_behavior', 'network_traffic')
        """
        try:
            # Extract features based on data type
            X = []
            for sample in training_data:
                if data_type == 'user_behavior':
                    features = self.extract_behavioral_features(sample)
                elif data_type == 'network_traffic':
                    features = self.extract_network_features(sample)
                else:
                    raise ValueError(f"Unsupported data type: {data_type}")
                
                X.append(features.flatten())
            
            X = np.array(X)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model based on method
            if self.method == 'isolation_forest':
                self.model.fit(X_scaled)
            elif self.method == 'dbscan':
                # DBSCAN doesn't have a fit method, we'll use it directly in predict
                pass
            elif self.method == 'statistical':
                # Calculate statistical baseline
                self.baseline_stats = {
                    'mean': np.mean(X_scaled, axis=0),
                    'std': np.std(X_scaled, axis=0),
                    'percentiles': {
                        '95': np.percentile(X_scaled, 95, axis=0),
                        '99': np.percentile(X_scaled, 99, axis=0)
                    }
                }
            
            self.is_trained = True
            self.data_type = data_type
            self.logger.info(f"Anomaly detector trained on {len(X)} samples")
            
        except Exception as e:
            self.logger.error(f"Error training anomaly detector: {str(e)}")
            raise
    
    def detect_anomaly(self, data):
        """
        Detect if the given data represents an anomaly.
        
        Args:
            data (dict): Data to analyze
            
        Returns:
            dict: Anomaly detection results
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before detecting anomalies")
        
        try:
            # Extract features
            if self.data_type == 'user_behavior':
                features = self.extract_behavioral_features(data)
            elif self.data_type == 'network_traffic':
                features = self.extract_network_features(data)
            
            features_scaled = self.scaler.transform(features)
            
            # Detect anomaly based on method
            if self.method == 'isolation_forest':
                prediction = self.model.predict(features_scaled)[0]
                anomaly_score = self.model.decision_function(features_scaled)[0]
                
                is_anomaly = prediction == -1
                confidence = abs(anomaly_score)
                
            elif self.method == 'dbscan':
                # Use DBSCAN to identify outliers
                labels = self.model.fit_predict(features_scaled)
                is_anomaly = labels[0] == -1  # -1 indicates outlier in DBSCAN
                confidence = 0.8 if is_anomaly else 0.2  # Simple confidence score
                
            elif self.method == 'statistical':
                # Statistical anomaly detection
                features_flat = features_scaled.flatten()
                z_scores = np.abs((features_flat - self.baseline_stats['mean']) / 
                                (self.baseline_stats['std'] + 1e-8))
                
                # Check if any feature exceeds threshold
                threshold = 3.0  # 3 standard deviations
                is_anomaly = np.any(z_scores > threshold)
                confidence = np.max(z_scores) / threshold if is_anomaly else np.max(z_scores) / threshold
                confidence = min(confidence, 1.0)
            
            # Calculate severity based on confidence
            if confidence > 0.8:
                severity = 'high'
            elif confidence > 0.6:
                severity = 'medium'
            else:
                severity = 'low'
            
            return {
                'is_anomaly': is_anomaly,
                'confidence': float(confidence),
                'severity': severity,
                'method': self.method,
                'data_type': self.data_type,
                'timestamp': datetime.utcnow().isoformat(),
                'details': {
                    'feature_count': len(features_scaled.flatten()),
                    'anomaly_score': float(anomaly_score) if self.method == 'isolation_forest' else None
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting anomaly: {str(e)}")
            raise
    
    def detect_time_series_anomalies(self, time_series_data, window_size=24):
        """
        Detect anomalies in time series data.
        
        Args:
            time_series_data (list): List of time-stamped data points
            window_size (int): Size of the sliding window for analysis
            
        Returns:
            list: List of anomaly detection results for each time point
        """
        results = []
        
        try:
            # Sort data by timestamp
            sorted_data = sorted(time_series_data, key=lambda x: x['timestamp'])
            
            for i in range(len(sorted_data)):
                # Get current data point
                current_data = sorted_data[i]
                
                # Get historical window
                start_idx = max(0, i - window_size)
                window_data = sorted_data[start_idx:i]
                
                if len(window_data) < window_size // 2:
                    # Not enough historical data
                    results.append({
                        'timestamp': current_data['timestamp'],
                        'is_anomaly': False,
                        'confidence': 0.0,
                        'reason': 'insufficient_historical_data'
                    })
                    continue
                
                # Extract values for statistical analysis
                values = [item.get('value', 0) for item in window_data]
                current_value = current_data.get('value', 0)
                
                # Calculate statistical measures
                mean_val = np.mean(values)
                std_val = np.std(values)
                
                if std_val == 0:
                    z_score = 0
                else:
                    z_score = abs(current_value - mean_val) / std_val
                
                # Determine if anomaly
                threshold = 2.5  # 2.5 standard deviations
                is_anomaly = z_score > threshold
                confidence = min(z_score / threshold, 1.0) if is_anomaly else z_score / threshold
                
                results.append({
                    'timestamp': current_data['timestamp'],
                    'is_anomaly': is_anomaly,
                    'confidence': float(confidence),
                    'z_score': float(z_score),
                    'threshold': threshold,
                    'value': current_value,
                    'baseline_mean': float(mean_val),
                    'baseline_std': float(std_val)
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in time series anomaly detection: {str(e)}")
            raise
    
    def generate_sample_data(self, num_samples=1000, data_type='user_behavior'):
        """
        Generate sample data for testing and training.
        
        Args:
            num_samples (int): Number of samples to generate
            data_type (str): Type of data to generate
            
        Returns:
            list: Generated sample data
        """
        np.random.seed(42)
        samples = []
        
        for i in range(num_samples):
            if data_type == 'user_behavior':
                # Generate normal user behavior
                sample = {
                    'login_times': [
                        (datetime.now() - timedelta(hours=np.random.randint(0, 24))).isoformat()
                        for _ in range(np.random.randint(1, 5))
                    ],
                    'files_accessed': np.random.randint(5, 50),
                    'applications_used': np.random.randint(3, 15),
                    'data_downloaded_mb': np.random.exponential(10),
                    'data_uploaded_mb': np.random.exponential(5),
                    'failed_access_attempts': np.random.randint(0, 3),
                    'unique_ips_accessed': np.random.randint(1, 10),
                    'external_connections': np.random.randint(0, 5),
                    'suspicious_domains_accessed': 0 if np.random.random() > 0.1 else np.random.randint(1, 3),
                    'bandwidth_usage_mb': np.random.normal(100, 30),
                    'session_durations': [
                        np.random.normal(3600, 600) for _ in range(np.random.randint(1, 5))
                    ]
                }
                
                # Add some anomalous samples (10%)
                if i > num_samples * 0.9:
                    sample.update({
                        'files_accessed': np.random.randint(100, 500),  # Excessive file access
                        'data_downloaded_mb': np.random.exponential(100),  # Large downloads
                        'failed_access_attempts': np.random.randint(10, 50),  # Many failures
                        'suspicious_domains_accessed': np.random.randint(5, 20),  # Suspicious activity
                        'bandwidth_usage_mb': np.random.normal(1000, 200)  # High bandwidth
                    })
                
            elif data_type == 'network_traffic':
                # Generate normal network traffic
                sample = {
                    'bytes_in': np.random.normal(1000000, 200000),
                    'bytes_out': np.random.normal(500000, 100000),
                    'packets_in': np.random.normal(1000, 200),
                    'packets_out': np.random.normal(800, 150),
                    'tcp_connections': np.random.randint(10, 100),
                    'udp_connections': np.random.randint(5, 50),
                    'failed_connections': np.random.randint(0, 10),
                    'unique_destinations': np.random.randint(5, 50),
                    'protocol_distribution': {
                        'http': np.random.randint(20, 60),
                        'https': np.random.randint(30, 70),
                        'ftp': np.random.randint(0, 10),
                        'ssh': np.random.randint(0, 5),
                        'dns': np.random.randint(10, 30)
                    },
                    'avg_connection_duration': np.random.normal(30, 10),
                    'peak_bandwidth_mbps': np.random.normal(10, 3),
                    'connection_frequency': np.random.normal(0.5, 0.2)
                }
                
                # Add some anomalous samples (10%)
                if i > num_samples * 0.9:
                    sample.update({
                        'bytes_in': np.random.normal(10000000, 2000000),  # High traffic
                        'failed_connections': np.random.randint(50, 200),  # Many failures
                        'unique_destinations': np.random.randint(200, 1000),  # Many destinations
                        'peak_bandwidth_mbps': np.random.normal(100, 20)  # High bandwidth
                    })
            
            samples.append(sample)
        
        return samples

