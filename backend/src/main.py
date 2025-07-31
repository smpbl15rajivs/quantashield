import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.asset import asset_bp
from src.routes.incident import incident_bp
from src.routes.risk import risk_bp
from src.routes.threat_intelligence import threat_intelligence_bp
from src.routes.compliance import compliance_bp
from src.routes.dashboard import dashboard_bp
from src.routes.monitoring import monitoring_bp
from src.routes.oauth import oauth_bp, init_oauth_service

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

# Enable CORS for all routes
CORS(app, origins="*")

# Initialize JWT
jwt = JWTManager(app)

# Initialize OAuth service
init_oauth_service(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(asset_bp, url_prefix='/api')
app.register_blueprint(incident_bp, url_prefix='/api')
app.register_blueprint(risk_bp, url_prefix='/api')
app.register_blueprint(threat_intelligence_bp, url_prefix='/api')
app.register_blueprint(compliance_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')
app.register_blueprint(monitoring_bp, url_prefix='/')
app.register_blueprint(oauth_bp)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Initialize services
try:
    from src.services.real_time_monitoring import monitoring_service
    from src.services.underground_intelligence import underground_intel_service
    
    # Start monitoring service
    monitoring_service.start_monitoring()
    print("✓ Real-time monitoring service started")
    print("✓ Underground intelligence service initialized")
except Exception as e:
    print(f"Warning: Could not initialize services: {e}")

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        from src.services.real_time_monitoring import monitoring_service
        from src.services.underground_intelligence import underground_intel_service
        
        return jsonify({
            'status': 'healthy',
            'service': 'QuantaShield Backend',
            'version': '1.0.0',
            'monitoring': monitoring_service.get_monitoring_status()['active'],
            'intelligence_sources': underground_intel_service.get_source_status()['active_sources'],
            'oauth_providers': ['google', 'microsoft', 'facebook', 'linkedin', 'twitter']
        })
    except Exception as e:
        return jsonify({
            'status': 'healthy',
            'service': 'QuantaShield Backend',
            'version': '1.0.0',
            'warning': f'Services not fully initialized: {e}'
        })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
