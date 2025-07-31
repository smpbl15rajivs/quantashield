"""
Real-time Monitoring Service
Handles real-time security monitoring, alerts, and event processing
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
import threading
import time
from queue import Queue
import uuid

@dataclass
class SecurityEvent:
    id: str
    event_type: str
    severity: str
    source: str
    description: str
    timestamp: datetime
    metadata: Dict[str, Any]
    status: str = 'new'

@dataclass
class Alert:
    id: str
    title: str
    description: str
    severity: str
    source: str
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False

class RealTimeMonitoringService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.event_queue = Queue()
        self.alerts = []
        self.subscribers = {}
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Event processors
        self.event_processors = {
            'login_attempt': self._process_login_event,
            'malware_detection': self._process_malware_event,
            'network_anomaly': self._process_network_event,
            'data_exfiltration': self._process_data_exfil_event,
            'unauthorized_access': self._process_access_event
        }
        
        # Initialize with sample events
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample security events and alerts"""
        sample_events = [
            SecurityEvent(
                id=str(uuid.uuid4()),
                event_type='login_attempt',
                severity='high',
                source='Web Server 01',
                description='Multiple failed login attempts from suspicious IP',
                timestamp=datetime.now() - timedelta(minutes=2),
                metadata={
                    'ip_address': '192.168.1.100',
                    'username': 'admin',
                    'attempts': 5,
                    'geolocation': 'Unknown'
                }
            ),
            SecurityEvent(
                id=str(uuid.uuid4()),
                event_type='malware_detection',
                severity='critical',
                source='Workstation 45',
                description='Malware detected and contained',
                timestamp=datetime.now() - timedelta(minutes=15),
                metadata={
                    'malware_type': 'Trojan',
                    'file_path': 'C:\\Users\\user\\Downloads\\malicious.exe',
                    'hash': 'a1b2c3d4e5f67890',
                    'action_taken': 'quarantined'
                }
            ),
            SecurityEvent(
                id=str(uuid.uuid4()),
                event_type='network_anomaly',
                severity='medium',
                source='Network Monitor',
                description='Unusual network traffic pattern detected',
                timestamp=datetime.now() - timedelta(hours=1),
                metadata={
                    'traffic_volume': '150% above baseline',
                    'protocol': 'HTTPS',
                    'destination': 'external',
                    'duration': '45 minutes'
                }
            )
        ]
        
        # Convert events to alerts
        for event in sample_events:
            alert = Alert(
                id=str(uuid.uuid4()),
                title=event.description,
                description=f"{event.event_type.replace('_', ' ').title()} from {event.source}",
                severity=event.severity,
                source=event.source,
                timestamp=event.timestamp
            )
            self.alerts.append(alert)
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            self.logger.info("Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("Real-time monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Process events from queue
                while not self.event_queue.empty():
                    event = self.event_queue.get()
                    self._process_event(event)
                
                # Generate simulated events periodically
                if self._should_generate_event():
                    event = self._generate_simulated_event()
                    self._process_event(event)
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(5)  # Wait before retrying
    
    def _should_generate_event(self) -> bool:
        """Determine if a simulated event should be generated"""
        import random
        # Generate event with 1% probability each second
        return random.random() < 0.01
    
    def _generate_simulated_event(self) -> SecurityEvent:
        """Generate a simulated security event"""
        import random
        
        event_types = ['login_attempt', 'network_anomaly', 'malware_detection', 'unauthorized_access']
        severities = ['low', 'medium', 'high', 'critical']
        sources = ['Web Server 01', 'Database Server', 'Workstation 45', 'Network Router', 'Firewall']
        
        event_type = random.choice(event_types)
        severity = random.choice(severities)
        source = random.choice(sources)
        
        descriptions = {
            'login_attempt': f'Suspicious login activity detected on {source}',
            'network_anomaly': f'Unusual network traffic from {source}',
            'malware_detection': f'Potential malware detected on {source}',
            'unauthorized_access': f'Unauthorized access attempt to {source}'
        }
        
        return SecurityEvent(
            id=str(uuid.uuid4()),
            event_type=event_type,
            severity=severity,
            source=source,
            description=descriptions[event_type],
            timestamp=datetime.now(),
            metadata={
                'generated': True,
                'random_id': random.randint(1000, 9999)
            }
        )
    
    def _process_event(self, event: SecurityEvent):
        """Process a security event"""
        try:
            # Log the event
            self.logger.info(f"Processing event: {event.event_type} - {event.severity} - {event.description}")
            
            # Use specific processor if available
            if event.event_type in self.event_processors:
                processor = self.event_processors[event.event_type]
                processor(event)
            else:
                self._process_generic_event(event)
            
            # Create alert if severity is high enough
            if event.severity in ['high', 'critical']:
                self._create_alert(event)
            
            # Notify subscribers
            self._notify_subscribers(event)
            
        except Exception as e:
            self.logger.error(f"Error processing event {event.id}: {str(e)}")
    
    def _process_login_event(self, event: SecurityEvent):
        """Process login-related events"""
        metadata = event.metadata
        if metadata.get('attempts', 0) > 3:
            event.severity = 'high'
            # Could trigger IP blocking here
    
    def _process_malware_event(self, event: SecurityEvent):
        """Process malware detection events"""
        event.severity = 'critical'  # Always critical
        # Could trigger automatic isolation here
    
    def _process_network_event(self, event: SecurityEvent):
        """Process network anomaly events"""
        # Analyze traffic patterns
        pass
    
    def _process_data_exfil_event(self, event: SecurityEvent):
        """Process data exfiltration events"""
        event.severity = 'critical'
        # Could trigger data loss prevention measures
    
    def _process_access_event(self, event: SecurityEvent):
        """Process unauthorized access events"""
        # Could trigger access control measures
        pass
    
    def _process_generic_event(self, event: SecurityEvent):
        """Process generic security events"""
        # Default processing
        pass
    
    def _create_alert(self, event: SecurityEvent):
        """Create an alert from a security event"""
        alert = Alert(
            id=str(uuid.uuid4()),
            title=event.description,
            description=f"{event.event_type.replace('_', ' ').title()} detected on {event.source}",
            severity=event.severity,
            source=event.source,
            timestamp=event.timestamp
        )
        
        self.alerts.append(alert)
        self.logger.info(f"Alert created: {alert.title}")
    
    def _notify_subscribers(self, event: SecurityEvent):
        """Notify all subscribers of a new event"""
        for subscriber_id, callback in self.subscribers.items():
            try:
                callback(event)
            except Exception as e:
                self.logger.error(f"Error notifying subscriber {subscriber_id}: {str(e)}")
    
    def subscribe(self, subscriber_id: str, callback: Callable[[SecurityEvent], None]):
        """Subscribe to real-time events"""
        self.subscribers[subscriber_id] = callback
        self.logger.info(f"Subscriber {subscriber_id} registered")
    
    def unsubscribe(self, subscriber_id: str):
        """Unsubscribe from real-time events"""
        if subscriber_id in self.subscribers:
            del self.subscribers[subscriber_id]
            self.logger.info(f"Subscriber {subscriber_id} unregistered")
    
    def add_event(self, event: SecurityEvent):
        """Add a new security event to the processing queue"""
        self.event_queue.put(event)
    
    def get_recent_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent security events"""
        # For demo purposes, return simulated recent events
        events = []
        for i in range(min(limit, 10)):
            event = self._generate_simulated_event()
            event.timestamp = datetime.now() - timedelta(minutes=i*5)
            events.append({
                'id': event.id,
                'event_type': event.event_type,
                'severity': event.severity,
                'source': event.source,
                'description': event.description,
                'timestamp': event.timestamp.isoformat(),
                'metadata': event.metadata,
                'status': event.status
            })
        
        return events
    
    def get_alerts(self, unresolved_only: bool = False) -> List[Dict[str, Any]]:
        """Get security alerts"""
        alerts = self.alerts.copy()
        
        if unresolved_only:
            alerts = [a for a in alerts if not a.resolved]
        
        # Sort by timestamp (newest first)
        alerts.sort(key=lambda x: x.timestamp, reverse=True)
        
        return [{
            'id': alert.id,
            'title': alert.title,
            'description': alert.description,
            'severity': alert.severity,
            'source': alert.source,
            'timestamp': alert.timestamp.isoformat(),
            'acknowledged': alert.acknowledged,
            'resolved': alert.resolved
        } for alert in alerts]
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                self.logger.info(f"Alert {alert_id} acknowledged")
                return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                alert.acknowledged = True
                self.logger.info(f"Alert {alert_id} resolved")
                return True
        return False
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            'active': self.monitoring_active,
            'events_processed': len(self.get_recent_events()),
            'active_alerts': len([a for a in self.alerts if not a.resolved]),
            'subscribers': len(self.subscribers),
            'uptime': 'Active' if self.monitoring_active else 'Inactive',
            'last_event': datetime.now().isoformat()
        }

# Global instance
monitoring_service = RealTimeMonitoringService()

