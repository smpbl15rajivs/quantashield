import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import logging
from datetime import datetime, timedelta
import joblib

class RiskAnalyzer:
    """
    AI/ML model for analyzing and predicting cybersecurity risks.
    Provides risk scoring and trend analysis capabilities.
    """
    
    def __init__(self, model_type='random_forest'):
        """
        Initialize the risk analyzer.
        
        Args:
            model_type (str): Type of model to use ('random_forest', 'gradient_boosting')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        self.feature_names = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize model based on type
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=6,
                learning_rate=0.1
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def extract_risk_features(self, risk_data):
        """
        Extract features from risk assessment data.
        
        Args:
            risk_data (dict): Risk assessment data
            
        Returns:
            np.array: Feature vector
        """
        features = []
        
        # Asset-related features
        asset_info = risk_data.get('asset', {})
        features.extend([
            self._encode_categorical('asset_type', asset_info.get('type', 'unknown')),
            self._encode_categorical('asset_criticality', asset_info.get('criticality', 'medium')),
            asset_info.get('age_years', 0),
            asset_info.get('patch_level', 0),  # 0-100 scale
            asset_info.get('exposure_score', 50)  # 0-100 scale
        ])
        
        # Vulnerability features
        vulnerabilities = risk_data.get('vulnerabilities', [])
        if vulnerabilities:
            cvss_scores = [v.get('cvss_score', 0) for v in vulnerabilities]
            features.extend([
                len(vulnerabilities),  # Count
                max(cvss_scores) if cvss_scores else 0,  # Highest CVSS
                np.mean(cvss_scores) if cvss_scores else 0,  # Average CVSS
                sum(1 for v in vulnerabilities if v.get('severity') == 'critical'),
                sum(1 for v in vulnerabilities if v.get('severity') == 'high'),
                sum(1 for v in vulnerabilities if v.get('exploitable', False))
            ])
        else:
            features.extend([0, 0, 0, 0, 0, 0])
        
        # Threat intelligence features
        threat_intel = risk_data.get('threat_intelligence', {})
        features.extend([
            threat_intel.get('active_campaigns', 0),
            threat_intel.get('targeting_score', 0),  # 0-100 scale
            threat_intel.get('threat_actor_interest', 0),  # 0-100 scale
            threat_intel.get('exploit_availability', 0)  # 0-1 scale
        ])
        
        # Historical incident features
        incidents = risk_data.get('historical_incidents', [])
        if incidents:
            recent_incidents = [i for i in incidents 
                             if datetime.fromisoformat(i.get('date', '2020-01-01')) > 
                             datetime.now() - timedelta(days=365)]
            features.extend([
                len(incidents),  # Total incidents
                len(recent_incidents),  # Recent incidents (last year)
                sum(1 for i in incidents if i.get('severity') == 'critical'),
                sum(1 for i in incidents if i.get('impact') == 'high'),
                np.mean([i.get('resolution_time_hours', 0) for i in incidents]) if incidents else 0
            ])
        else:
            features.extend([0, 0, 0, 0, 0])
        
        # Network exposure features
        network = risk_data.get('network_exposure', {})
        features.extend([
            network.get('internet_facing', 0),  # 0 or 1
            network.get('open_ports', 0),
            network.get('weak_protocols', 0),
            network.get('firewall_rules', 0),
            network.get('network_segmentation', 0)  # 0-100 scale
        ])
        
        # Compliance features
        compliance = risk_data.get('compliance', {})
        features.extend([
            compliance.get('overall_score', 50),  # 0-100 scale
            compliance.get('critical_controls_missing', 0),
            compliance.get('audit_findings', 0),
            compliance.get('policy_violations', 0)
        ])
        
        # User behavior features
        user_behavior = risk_data.get('user_behavior', {})
        features.extend([
            user_behavior.get('privileged_users', 0),
            user_behavior.get('anomalous_activities', 0),
            user_behavior.get('failed_authentications', 0),
            user_behavior.get('data_access_violations', 0),
            user_behavior.get('security_training_score', 50)  # 0-100 scale
        ])
        
        return np.array(features).reshape(1, -1)
    
    def _encode_categorical(self, feature_name, value):
        """
        Encode categorical values using label encoding.
        
        Args:
            feature_name (str): Name of the feature
            value (str): Categorical value to encode
            
        Returns:
            int: Encoded value
        """
        if feature_name not in self.label_encoders:
            self.label_encoders[feature_name] = LabelEncoder()
            # Fit with common values to ensure consistency
            if feature_name == 'asset_type':
                common_values = ['server', 'workstation', 'network_device', 'database', 'application', 'unknown']
            elif feature_name == 'asset_criticality':
                common_values = ['low', 'medium', 'high', 'critical']
            else:
                common_values = [value, 'unknown']
            
            self.label_encoders[feature_name].fit(common_values)
        
        try:
            return self.label_encoders[feature_name].transform([value])[0]
        except ValueError:
            # Handle unseen values by encoding as 'unknown'
            return self.label_encoders[feature_name].transform(['unknown'])[0]
    
    def train(self, training_data, risk_scores):
        """
        Train the risk analysis model.
        
        Args:
            training_data (list): List of risk assessment data
            risk_scores (list): Corresponding risk scores (0-100)
        """
        try:
            # Prepare feature matrix
            X = []
            for sample in training_data:
                features = self.extract_risk_features(sample)
                X.append(features.flatten())
            
            X = np.array(X)
            y = np.array(risk_scores)
            
            # Store feature names for later reference
            self.feature_names = [
                'asset_type', 'asset_criticality', 'asset_age', 'patch_level', 'exposure_score',
                'vuln_count', 'max_cvss', 'avg_cvss', 'critical_vulns', 'high_vulns', 'exploitable_vulns',
                'active_campaigns', 'targeting_score', 'threat_actor_interest', 'exploit_availability',
                'total_incidents', 'recent_incidents', 'critical_incidents', 'high_impact_incidents', 'avg_resolution_time',
                'internet_facing', 'open_ports', 'weak_protocols', 'firewall_rules', 'network_segmentation',
                'compliance_score', 'critical_controls_missing', 'audit_findings', 'policy_violations',
                'privileged_users', 'anomalous_activities', 'failed_authentications', 'data_access_violations', 'security_training_score'
            ]
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Split data for training and validation
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.logger.info(f"Model trained successfully:")
            self.logger.info(f"MSE: {mse:.2f}, R²: {r2:.3f}")
            
            self.is_trained = True
            
        except Exception as e:
            self.logger.error(f"Error training risk analyzer: {str(e)}")
            raise
    
    def analyze_risk(self, risk_data):
        """
        Analyze risk for the given data.
        
        Args:
            risk_data (dict): Risk assessment data
            
        Returns:
            dict: Risk analysis results
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before analyzing risk")
        
        try:
            # Extract features
            features = self.extract_risk_features(risk_data)
            features_scaled = self.scaler.transform(features)
            
            # Predict risk score
            risk_score = self.model.predict(features_scaled)[0]
            risk_score = max(0, min(100, risk_score))  # Clamp to 0-100 range
            
            # Determine risk level
            if risk_score >= 80:
                risk_level = 'critical'
            elif risk_score >= 60:
                risk_level = 'high'
            elif risk_score >= 40:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            # Get feature importance
            feature_importance = None
            if hasattr(self.model, 'feature_importances_'):
                importance_scores = self.model.feature_importances_
                feature_importance = dict(zip(self.feature_names, importance_scores))
                # Sort by importance and get top 5
                feature_importance = dict(sorted(
                    feature_importance.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5])
            
            # Generate recommendations
            recommendations = self._generate_recommendations(risk_data, risk_score, feature_importance)
            
            return {
                'risk_score': float(risk_score),
                'risk_level': risk_level,
                'model_type': self.model_type,
                'timestamp': datetime.utcnow().isoformat(),
                'feature_importance': feature_importance,
                'recommendations': recommendations,
                'confidence': self._calculate_confidence(features_scaled)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing risk: {str(e)}")
            raise
    
    def _calculate_confidence(self, features):
        """
        Calculate confidence in the risk prediction.
        
        Args:
            features (np.array): Scaled feature vector
            
        Returns:
            float: Confidence score (0-1)
        """
        # For ensemble models, use prediction variance as confidence indicator
        if hasattr(self.model, 'estimators_'):
            predictions = [estimator.predict(features)[0] for estimator in self.model.estimators_]
            variance = np.var(predictions)
            # Convert variance to confidence (lower variance = higher confidence)
            confidence = 1.0 / (1.0 + variance / 100)  # Normalize by typical risk score range
            return min(max(confidence, 0.0), 1.0)
        else:
            return 0.8  # Default confidence for non-ensemble models
    
    def _generate_recommendations(self, risk_data, risk_score, feature_importance):
        """
        Generate risk mitigation recommendations.
        
        Args:
            risk_data (dict): Original risk data
            risk_score (float): Calculated risk score
            feature_importance (dict): Feature importance scores
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        # High-level recommendations based on risk score
        if risk_score >= 80:
            recommendations.append("Immediate action required - Critical risk level detected")
        elif risk_score >= 60:
            recommendations.append("High priority - Address identified vulnerabilities promptly")
        
        # Specific recommendations based on feature importance
        if feature_importance:
            top_feature = list(feature_importance.keys())[0]
            
            if 'vuln' in top_feature.lower():
                recommendations.append("Prioritize vulnerability management and patching")
            elif 'compliance' in top_feature.lower():
                recommendations.append("Improve compliance posture and address control gaps")
            elif 'incident' in top_feature.lower():
                recommendations.append("Strengthen incident response capabilities")
            elif 'network' in top_feature.lower():
                recommendations.append("Review and enhance network security controls")
            elif 'user' in top_feature.lower():
                recommendations.append("Implement additional user behavior monitoring")
        
        # Data-driven recommendations
        vulnerabilities = risk_data.get('vulnerabilities', [])
        if vulnerabilities:
            critical_vulns = sum(1 for v in vulnerabilities if v.get('severity') == 'critical')
            if critical_vulns > 0:
                recommendations.append(f"Address {critical_vulns} critical vulnerabilities immediately")
        
        network = risk_data.get('network_exposure', {})
        if network.get('internet_facing', 0) > 0:
            recommendations.append("Review internet-facing assets and minimize exposure")
        
        compliance = risk_data.get('compliance', {})
        if compliance.get('overall_score', 50) < 70:
            recommendations.append("Improve compliance score through control implementation")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def predict_risk_trend(self, historical_data, forecast_days=30):
        """
        Predict risk trend based on historical data.
        
        Args:
            historical_data (list): Historical risk scores with timestamps
            forecast_days (int): Number of days to forecast
            
        Returns:
            dict: Risk trend prediction
        """
        try:
            if len(historical_data) < 7:
                return {
                    'trend': 'insufficient_data',
                    'forecast': [],
                    'confidence': 0.0
                }
            
            # Extract timestamps and risk scores
            dates = [datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00')) 
                    for item in historical_data]
            scores = [item['risk_score'] for item in historical_data]
            
            # Sort by date
            sorted_data = sorted(zip(dates, scores))
            dates, scores = zip(*sorted_data)
            
            # Simple linear trend analysis
            x = np.arange(len(scores))
            coeffs = np.polyfit(x, scores, 1)
            trend_slope = coeffs[0]
            
            # Determine trend direction
            if trend_slope > 1:
                trend = 'increasing'
            elif trend_slope < -1:
                trend = 'decreasing'
            else:
                trend = 'stable'
            
            # Generate forecast
            forecast = []
            last_date = dates[-1]
            last_score = scores[-1]
            
            for i in range(1, forecast_days + 1):
                forecast_date = last_date + timedelta(days=i)
                forecast_score = last_score + (trend_slope * i)
                forecast_score = max(0, min(100, forecast_score))  # Clamp to valid range
                
                forecast.append({
                    'date': forecast_date.isoformat(),
                    'predicted_risk_score': float(forecast_score)
                })
            
            # Calculate confidence based on data consistency
            score_variance = np.var(scores)
            confidence = 1.0 / (1.0 + score_variance / 100)
            confidence = min(max(confidence, 0.0), 1.0)
            
            return {
                'trend': trend,
                'trend_slope': float(trend_slope),
                'forecast': forecast,
                'confidence': float(confidence),
                'historical_variance': float(score_variance)
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting risk trend: {str(e)}")
            raise
    
    def generate_sample_data(self, num_samples=1000):
        """
        Generate sample risk assessment data for training.
        
        Args:
            num_samples (int): Number of samples to generate
            
        Returns:
            tuple: (training_data, risk_scores)
        """
        np.random.seed(42)
        training_data = []
        risk_scores = []
        
        asset_types = ['server', 'workstation', 'network_device', 'database', 'application']
        criticality_levels = ['low', 'medium', 'high', 'critical']
        
        for i in range(num_samples):
            # Generate base risk factors
            asset_criticality = np.random.choice(criticality_levels)
            vuln_count = np.random.poisson(5)
            
            sample = {
                'asset': {
                    'type': np.random.choice(asset_types),
                    'criticality': asset_criticality,
                    'age_years': np.random.randint(0, 10),
                    'patch_level': np.random.randint(0, 100),
                    'exposure_score': np.random.randint(0, 100)
                },
                'vulnerabilities': [
                    {
                        'cvss_score': np.random.uniform(1, 10),
                        'severity': np.random.choice(['low', 'medium', 'high', 'critical']),
                        'exploitable': np.random.random() > 0.7
                    } for _ in range(vuln_count)
                ],
                'threat_intelligence': {
                    'active_campaigns': np.random.randint(0, 10),
                    'targeting_score': np.random.randint(0, 100),
                    'threat_actor_interest': np.random.randint(0, 100),
                    'exploit_availability': np.random.random()
                },
                'historical_incidents': [
                    {
                        'date': (datetime.now() - timedelta(days=np.random.randint(0, 730))).isoformat(),
                        'severity': np.random.choice(['low', 'medium', 'high', 'critical']),
                        'impact': np.random.choice(['low', 'medium', 'high']),
                        'resolution_time_hours': np.random.exponential(24)
                    } for _ in range(np.random.randint(0, 5))
                ],
                'network_exposure': {
                    'internet_facing': np.random.randint(0, 2),
                    'open_ports': np.random.randint(0, 50),
                    'weak_protocols': np.random.randint(0, 10),
                    'firewall_rules': np.random.randint(0, 100),
                    'network_segmentation': np.random.randint(0, 100)
                },
                'compliance': {
                    'overall_score': np.random.randint(0, 100),
                    'critical_controls_missing': np.random.randint(0, 20),
                    'audit_findings': np.random.randint(0, 50),
                    'policy_violations': np.random.randint(0, 30)
                },
                'user_behavior': {
                    'privileged_users': np.random.randint(1, 20),
                    'anomalous_activities': np.random.randint(0, 10),
                    'failed_authentications': np.random.randint(0, 100),
                    'data_access_violations': np.random.randint(0, 20),
                    'security_training_score': np.random.randint(0, 100)
                }
            }
            
            # Calculate risk score based on factors
            base_score = 30
            
            # Asset criticality impact
            criticality_impact = {'low': 0, 'medium': 10, 'high': 20, 'critical': 30}
            base_score += criticality_impact[asset_criticality]
            
            # Vulnerability impact
            if vuln_count > 0:
                max_cvss = max([v['cvss_score'] for v in sample['vulnerabilities']])
                base_score += max_cvss * 3
                
                critical_vulns = sum(1 for v in sample['vulnerabilities'] if v['severity'] == 'critical')
                base_score += critical_vulns * 5
            
            # Other factors
            base_score += sample['network_exposure']['internet_facing'] * 10
            base_score += (100 - sample['compliance']['overall_score']) * 0.2
            base_score += len(sample['historical_incidents']) * 3
            
            # Add some noise
            base_score += np.random.normal(0, 5)
            
            # Clamp to valid range
            risk_score = max(0, min(100, base_score))
            
            training_data.append(sample)
            risk_scores.append(risk_score)
        
        return training_data, risk_scores

