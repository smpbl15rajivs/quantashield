import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import logging
from datetime import datetime
import os

class ThreatDetector:
    """
    AI/ML model for detecting cybersecurity threats using various algorithms.
    Supports both supervised and unsupervised learning approaches.
    """
    
    def __init__(self, model_type='isolation_forest'):
        """
        Initialize the threat detector.
        
        Args:
            model_type (str): Type of model to use ('isolation_forest', 'random_forest')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize model based on type
        if model_type == 'isolation_forest':
            self.model = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def prepare_features(self, data):
        """
        Prepare features from raw security data.
        
        Args:
            data (dict): Raw security data containing various metrics
            
        Returns:
            np.array: Processed feature vector
        """
        features = []
        
        # Network-based features
        if 'network_traffic' in data:
            traffic = data['network_traffic']
            features.extend([
                traffic.get('bytes_in', 0),
                traffic.get('bytes_out', 0),
                traffic.get('packets_in', 0),
                traffic.get('packets_out', 0),
                traffic.get('connections_count', 0),
                traffic.get('failed_connections', 0)
            ])
        else:
            features.extend([0] * 6)
        
        # User behavior features
        if 'user_behavior' in data:
            behavior = data['user_behavior']
            features.extend([
                behavior.get('login_attempts', 0),
                behavior.get('failed_logins', 0),
                behavior.get('session_duration', 0),
                behavior.get('files_accessed', 0),
                behavior.get('privilege_escalations', 0),
                behavior.get('off_hours_activity', 0)
            ])
        else:
            features.extend([0] * 6)
        
        # System-based features
        if 'system_metrics' in data:
            system = data['system_metrics']
            features.extend([
                system.get('cpu_usage', 0),
                system.get('memory_usage', 0),
                system.get('disk_usage', 0),
                system.get('process_count', 0),
                system.get('network_connections', 0)
            ])
        else:
            features.extend([0] * 5)
        
        # Log-based features
        if 'log_entries' in data:
            logs = data['log_entries']
            features.extend([
                len(logs) if isinstance(logs, list) else 0,
                sum(1 for log in logs if log.get('level') == 'ERROR') if isinstance(logs, list) else 0,
                sum(1 for log in logs if log.get('level') == 'WARNING') if isinstance(logs, list) else 0
            ])
        else:
            features.extend([0] * 3)
        
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data, labels=None):
        """
        Train the threat detection model.
        
        Args:
            training_data (list): List of training samples
            labels (list, optional): Labels for supervised learning
        """
        try:
            # Prepare feature matrix
            X = []
            for sample in training_data:
                features = self.prepare_features(sample)
                X.append(features.flatten())
            
            X = np.array(X)
            
            # Store feature names for later reference
            self.feature_names = [
                'bytes_in', 'bytes_out', 'packets_in', 'packets_out', 
                'connections_count', 'failed_connections',
                'login_attempts', 'failed_logins', 'session_duration',
                'files_accessed', 'privilege_escalations', 'off_hours_activity',
                'cpu_usage', 'memory_usage', 'disk_usage', 
                'process_count', 'network_connections',
                'log_count', 'error_logs', 'warning_logs'
            ]
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            if self.model_type == 'isolation_forest':
                # Unsupervised learning
                self.model.fit(X_scaled)
            elif self.model_type == 'random_forest' and labels is not None:
                # Supervised learning
                y = np.array(labels)
                X_train, X_test, y_train, y_test = train_test_split(
                    X_scaled, y, test_size=0.2, random_state=42
                )
                
                self.model.fit(X_train, y_train)
                
                # Evaluate model
                y_pred = self.model.predict(X_test)
                self.logger.info("Model Performance:")
                self.logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")
            
            self.is_trained = True
            self.logger.info(f"Model trained successfully with {len(X)} samples")
            
        except Exception as e:
            self.logger.error(f"Error training model: {str(e)}")
            raise
    
    def predict(self, data):
        """
        Predict if the given data represents a threat.
        
        Args:
            data (dict): Security data to analyze
            
        Returns:
            dict: Prediction results with confidence score
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        try:
            # Prepare features
            features = self.prepare_features(data)
            features_scaled = self.scaler.transform(features)
            
            # Make prediction
            if self.model_type == 'isolation_forest':
                # Isolation Forest returns -1 for anomalies, 1 for normal
                prediction = self.model.predict(features_scaled)[0]
                anomaly_score = self.model.decision_function(features_scaled)[0]
                
                is_threat = prediction == -1
                confidence = abs(anomaly_score)
                
            elif self.model_type == 'random_forest':
                # Random Forest returns class probabilities
                prediction = self.model.predict(features_scaled)[0]
                probabilities = self.model.predict_proba(features_scaled)[0]
                
                is_threat = prediction == 1
                confidence = max(probabilities)
            
            # Get feature importance if available
            feature_importance = None
            if hasattr(self.model, 'feature_importances_'):
                importance_scores = self.model.feature_importances_
                feature_importance = dict(zip(self.feature_names, importance_scores))
                # Sort by importance
                feature_importance = dict(sorted(
                    feature_importance.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:5])  # Top 5 features
            
            return {
                'is_threat': is_threat,
                'confidence': float(confidence),
                'threat_score': float(1 - confidence) if not is_threat else float(confidence),
                'model_type': self.model_type,
                'timestamp': datetime.utcnow().isoformat(),
                'feature_importance': feature_importance
            }
            
        except Exception as e:
            self.logger.error(f"Error making prediction: {str(e)}")
            raise
    
    def save_model(self, filepath):
        """
        Save the trained model to disk.
        
        Args:
            filepath (str): Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'model_type': self.model_type,
                'feature_names': self.feature_names,
                'is_trained': self.is_trained
            }
            
            joblib.dump(model_data, filepath)
            self.logger.info(f"Model saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")
            raise
    
    def load_model(self, filepath):
        """
        Load a trained model from disk.
        
        Args:
            filepath (str): Path to the saved model
        """
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Model file not found: {filepath}")
            
            model_data = joblib.load(filepath)
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.model_type = model_data['model_type']
            self.feature_names = model_data['feature_names']
            self.is_trained = model_data['is_trained']
            
            self.logger.info(f"Model loaded from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise
    
    def generate_sample_data(self, num_samples=1000):
        """
        Generate sample training data for demonstration purposes.
        
        Args:
            num_samples (int): Number of samples to generate
            
        Returns:
            tuple: (training_data, labels)
        """
        np.random.seed(42)
        training_data = []
        labels = []
        
        for i in range(num_samples):
            # Generate normal behavior (80% of samples)
            if i < num_samples * 0.8:
                sample = {
                    'network_traffic': {
                        'bytes_in': np.random.normal(1000, 200),
                        'bytes_out': np.random.normal(800, 150),
                        'packets_in': np.random.normal(50, 10),
                        'packets_out': np.random.normal(40, 8),
                        'connections_count': np.random.randint(1, 10),
                        'failed_connections': np.random.randint(0, 2)
                    },
                    'user_behavior': {
                        'login_attempts': np.random.randint(1, 3),
                        'failed_logins': np.random.randint(0, 1),
                        'session_duration': np.random.normal(3600, 600),
                        'files_accessed': np.random.randint(5, 20),
                        'privilege_escalations': 0,
                        'off_hours_activity': np.random.randint(0, 1)
                    },
                    'system_metrics': {
                        'cpu_usage': np.random.normal(30, 10),
                        'memory_usage': np.random.normal(50, 15),
                        'disk_usage': np.random.normal(60, 20),
                        'process_count': np.random.randint(50, 100),
                        'network_connections': np.random.randint(10, 30)
                    },
                    'log_entries': [
                        {'level': 'INFO'} for _ in range(np.random.randint(10, 30))
                    ]
                }
                labels.append(0)  # Normal
            else:
                # Generate anomalous behavior (20% of samples)
                sample = {
                    'network_traffic': {
                        'bytes_in': np.random.normal(5000, 1000),  # Higher traffic
                        'bytes_out': np.random.normal(4000, 800),
                        'packets_in': np.random.normal(200, 50),
                        'packets_out': np.random.normal(180, 40),
                        'connections_count': np.random.randint(20, 50),  # More connections
                        'failed_connections': np.random.randint(5, 15)  # More failures
                    },
                    'user_behavior': {
                        'login_attempts': np.random.randint(5, 20),  # More login attempts
                        'failed_logins': np.random.randint(3, 10),  # More failures
                        'session_duration': np.random.normal(7200, 1200),  # Longer sessions
                        'files_accessed': np.random.randint(50, 200),  # More files
                        'privilege_escalations': np.random.randint(1, 5),  # Privilege escalation
                        'off_hours_activity': 1  # Off-hours activity
                    },
                    'system_metrics': {
                        'cpu_usage': np.random.normal(80, 15),  # High CPU
                        'memory_usage': np.random.normal(90, 10),  # High memory
                        'disk_usage': np.random.normal(95, 5),  # High disk usage
                        'process_count': np.random.randint(200, 500),  # Many processes
                        'network_connections': np.random.randint(100, 300)  # Many connections
                    },
                    'log_entries': [
                        {'level': 'ERROR'} for _ in range(np.random.randint(20, 50))
                    ] + [
                        {'level': 'WARNING'} for _ in range(np.random.randint(10, 30))
                    ]
                }
                labels.append(1)  # Anomalous/Threat
            
            training_data.append(sample)
        
        return training_data, labels

