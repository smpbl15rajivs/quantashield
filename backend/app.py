from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'QuantaShield Backend API',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/auth/providers', methods=['GET'])
def get_providers():
    """Get list of available OAuth providers"""
    providers = [
        {
            'name': 'google',
            'display_name': 'Google',
            'icon': 'google',
            'color': '#4285f4'
        },
        {
            'name': 'microsoft',
            'display_name': 'Microsoft',
            'icon': 'microsoft',
            'color': '#00a1f1'
        },
        {
            'name': 'facebook',
            'display_name': 'Facebook',
            'icon': 'facebook',
            'color': '#1877f2'
        },
        {
            'name': 'linkedin',
            'display_name': 'LinkedIn',
            'icon': 'linkedin',
            'color': '#0077b5'
        },
        {
            'name': 'twitter',
            'display_name': 'Twitter',
            'icon': 'twitter',
            'color': '#1da1f2'
        }
    ]
    
    return jsonify({
        'success': True,
        'providers': providers
    })

@app.route('/api/auth/<provider>/login', methods=['GET'])
def oauth_login(provider):
    """Simulate OAuth login initiation"""
    return jsonify({
        'success': False,
        'error': 'OAuth configuration required. Please contact administrator to set up social login credentials.',
        'provider': provider
    }), 501

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Traditional login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Demo credentials
    if username == 'admin' and password == 'password':
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'username': username,
                'email': 'admin@quantashield.in'
            }
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Invalid credentials'
        }), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

