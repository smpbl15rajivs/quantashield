"""
Underground Intelligence Service
Handles data collection from dark web sources and underground channels
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
from concurrent.futures import ThreadPoolExecutor
import hashlib
import re

class UndergroundIntelligenceService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_sources = []
        self.credential_cache = {}
        self.threat_indicators = {}
        
        # Simulated underground sources
        self.sources = {
            'telegram_channels': [
                {'name': 'Telegram Channel Alpha', 'status': 'active', 'type': 'stealer_logs'},
                {'name': 'Underground Market Beta', 'status': 'active', 'type': 'credential_dumps'},
                {'name': 'Dark Web Forum Gamma', 'status': 'monitoring', 'type': 'threat_intel'},
                {'name': 'Stealer Log Delta', 'status': 'active', 'type': 'malware_logs'}
            ],
            'dark_web_forums': [
                {'name': 'Forum Alpha', 'url': 'hidden', 'status': 'active'},
                {'name': 'Market Beta', 'url': 'hidden', 'status': 'monitoring'},
                {'name': 'Channel Gamma', 'url': 'hidden', 'status': 'active'}
            ]
        }
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample underground intelligence data"""
        # Sample leaked credentials
        self.leaked_credentials = [
            {
                'id': 1,
                'email': 'john.doe@quantashield.in',
                'domain': 'quantashield.in',
                'password_hash': hashlib.sha256('password123'.encode()).hexdigest()[:16] + '...',
                'source': 'RedLine Stealer',
                'discovered': datetime.now() - timedelta(hours=2),
                'severity': 'high',
                'breach': 'Corporate Data Leak 2024',
                'additional_data': {
                    'browser_data': True,
                    'cookies': True,
                    'autofill': True
                }
            },
            {
                'id': 2,
                'email': 'admin@quantashield.in',
                'domain': 'quantashield.in',
                'password_hash': hashlib.sha256('admin2024'.encode()).hexdigest()[:16] + '...',
                'source': 'Raccoon Stealer',
                'discovered': datetime.now() - timedelta(hours=5),
                'severity': 'critical',
                'breach': 'Admin Panel Compromise',
                'additional_data': {
                    'system_info': True,
                    'network_data': True,
                    'crypto_wallets': False
                }
            },
            {
                'id': 3,
                'email': 'support@quantashield.in',
                'domain': 'quantashield.in',
                'password_hash': hashlib.sha256('support123'.encode()).hexdigest()[:16] + '...',
                'source': 'Meta Stealer',
                'discovered': datetime.now() - timedelta(hours=8),
                'severity': 'medium',
                'breach': 'Support System Breach',
                'additional_data': {
                    'browser_data': True,
                    'cookies': False,
                    'autofill': True
                }
            }
        ]
        
        # Sample threat indicators
        self.threat_indicators_data = [
            {
                'id': 1,
                'type': 'ip',
                'value': '192.168.1.100',
                'threat_type': 'malware',
                'confidence': 95,
                'first_seen': datetime.now() - timedelta(days=6),
                'last_seen': datetime.now() - timedelta(hours=1),
                'tags': ['botnet', 'c2-server', 'redline'],
                'source': 'Underground Forum Alpha'
            },
            {
                'id': 2,
                'type': 'domain',
                'value': 'malicious-site.example',
                'threat_type': 'phishing',
                'confidence': 88,
                'first_seen': datetime.now() - timedelta(days=4),
                'last_seen': datetime.now() - timedelta(hours=3),
                'tags': ['phishing', 'credential-theft', 'banking'],
                'source': 'Telegram Channel Beta'
            },
            {
                'id': 3,
                'type': 'hash',
                'value': 'a1b2c3d4e5f67890abcdef1234567890',
                'threat_type': 'malware',
                'confidence': 92,
                'first_seen': datetime.now() - timedelta(days=5),
                'last_seen': datetime.now() - timedelta(hours=2),
                'tags': ['trojan', 'data-exfil', 'stealer'],
                'source': 'Dark Web Market Gamma'
            }
        ]
    
    async def collect_intelligence(self) -> Dict[str, Any]:
        """Collect intelligence from all configured sources"""
        try:
            results = {
                'timestamp': datetime.now().isoformat(),
                'sources_checked': len(self.sources['telegram_channels']) + len(self.sources['dark_web_forums']),
                'new_credentials': 0,
                'new_indicators': 0,
                'status': 'success'
            }
            
            # Simulate collection process
            await asyncio.sleep(0.1)  # Simulate network delay
            
            # Process telegram channels
            for channel in self.sources['telegram_channels']:
                if channel['status'] == 'active':
                    new_data = await self._process_telegram_channel(channel)
                    results['new_credentials'] += new_data.get('credentials', 0)
                    results['new_indicators'] += new_data.get('indicators', 0)
            
            # Process dark web forums
            for forum in self.sources['dark_web_forums']:
                if forum['status'] == 'active':
                    new_data = await self._process_dark_web_forum(forum)
                    results['new_credentials'] += new_data.get('credentials', 0)
                    results['new_indicators'] += new_data.get('indicators', 0)
            
            self.logger.info(f"Intelligence collection completed: {results}")
            return results
            
        except Exception as e:
            self.logger.error(f"Intelligence collection failed: {str(e)}")
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    async def _process_telegram_channel(self, channel: Dict[str, Any]) -> Dict[str, int]:
        """Process a telegram channel for new intelligence"""
        # Simulate processing
        await asyncio.sleep(0.05)
        
        # Simulate finding new data
        import random
        return {
            'credentials': random.randint(0, 5),
            'indicators': random.randint(0, 3)
        }
    
    async def _process_dark_web_forum(self, forum: Dict[str, Any]) -> Dict[str, int]:
        """Process a dark web forum for new intelligence"""
        # Simulate processing
        await asyncio.sleep(0.05)
        
        # Simulate finding new data
        import random
        return {
            'credentials': random.randint(0, 3),
            'indicators': random.randint(0, 2)
        }
    
    def get_leaked_credentials(self, domain: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get leaked credentials, optionally filtered by domain"""
        credentials = self.leaked_credentials.copy()
        
        if domain:
            credentials = [c for c in credentials if c['domain'] == domain]
        
        # Sort by discovery date (newest first)
        credentials.sort(key=lambda x: x['discovered'], reverse=True)
        
        return credentials[:limit]
    
    def get_threat_indicators(self, indicator_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get threat indicators, optionally filtered by type"""
        indicators = self.threat_indicators_data.copy()
        
        if indicator_type:
            indicators = [i for i in indicators if i['type'] == indicator_type]
        
        # Sort by confidence (highest first)
        indicators.sort(key=lambda x: x['confidence'], reverse=True)
        
        return indicators[:limit]
    
    def get_source_status(self) -> Dict[str, Any]:
        """Get status of all intelligence sources"""
        total_sources = len(self.sources['telegram_channels']) + len(self.sources['dark_web_forums'])
        active_sources = 0
        
        for channel in self.sources['telegram_channels']:
            if channel['status'] == 'active':
                active_sources += 1
        
        for forum in self.sources['dark_web_forums']:
            if forum['status'] == 'active':
                active_sources += 1
        
        return {
            'total_sources': total_sources,
            'active_sources': active_sources,
            'uptime_percentage': round((active_sources / total_sources) * 100, 1),
            'last_update': datetime.now().isoformat(),
            'sources': {
                'telegram_channels': self.sources['telegram_channels'],
                'dark_web_forums': self.sources['dark_web_forums']
            }
        }
    
    def search_credentials(self, query: str) -> List[Dict[str, Any]]:
        """Search leaked credentials by email, domain, or other criteria"""
        results = []
        query_lower = query.lower()
        
        for cred in self.leaked_credentials:
            if (query_lower in cred['email'].lower() or 
                query_lower in cred['domain'].lower() or 
                query_lower in cred['source'].lower() or
                query_lower in cred['breach'].lower()):
                results.append(cred)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics for underground intelligence"""
        total_credentials = len(self.leaked_credentials)
        unique_domains = len(set(c['domain'] for c in self.leaked_credentials))
        total_indicators = len(self.threat_indicators_data)
        
        # Calculate severity distribution
        severity_counts = {}
        for cred in self.leaked_credentials:
            severity = cred['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            'total_credentials': total_credentials,
            'unique_domains': unique_domains,
            'total_indicators': total_indicators,
            'severity_distribution': severity_counts,
            'sources_online': self.get_source_status()['active_sources'],
            'last_updated': datetime.now().isoformat()
        }

# Global instance
underground_intel_service = UndergroundIntelligenceService()

