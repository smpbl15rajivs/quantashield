# QuantaShield - Enterprise Cybersecurity Platform

QuantaShield is a comprehensive cybersecurity platform designed for enterprise-level threat detection, incident response, and security management.

## 🚀 Features

- **Federated Authentication** - Support for Google, Microsoft, Facebook, LinkedIn, and Twitter login
- **Threat Intelligence** - Real-time threat monitoring and analysis
- **Incident Response** - Automated incident detection and response workflows
- **Asset Management** - Comprehensive asset inventory and vulnerability tracking
- **Compliance Monitoring** - Regulatory compliance tracking and reporting
- **User Management** - Role-based access control and user administration

## 🏗️ Architecture

### Backend (Flask API)
- **Location**: `/backend/`
- **Framework**: Python Flask
- **Database**: PostgreSQL
- **Authentication**: JWT with OAuth2 integration
- **API Documentation**: RESTful API with comprehensive endpoints

### Frontend (React Application)
- **Location**: `/frontend/`
- **Framework**: React 18 with modern hooks
- **UI Library**: Custom cybersecurity-themed components
- **State Management**: React Context API
- **Responsive Design**: Mobile-first approach

## 🛠️ Deployment

### Using Coolify (Recommended)
1. Connect this repository to Coolify
2. Deploy backend service with PostgreSQL database
3. Deploy frontend service with nginx
4. Configure environment variables
5. Set up domain routing

### Using Docker Compose
```bash
# Clone the repository
git clone https://github.com/smpbl15rajivs/quantashield.git
cd quantashield

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://quantashield:password@db:5432/quantashield
POSTGRES_DB=quantashield
POSTGRES_USER=quantashield
POSTGRES_PASSWORD=quantashield_secure_2025

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret
# ... other OAuth providers
```

## 📁 Project Structure

```
quantashield/
├── backend/                 # Flask API application
│   ├── src/
│   │   ├── routes/         # API route handlers
│   │   ├── services/       # Business logic services
│   │   ├── models/         # Database models
│   │   └── config/         # Configuration files
│   ├── app.py              # Flask application entry point
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container configuration
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service calls
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend container configuration
│   └── nginx.conf          # Nginx configuration
├── docs/                   # Documentation
├── docker-compose.yml      # Multi-service deployment
├── init.sql               # Database initialization
└── .env                   # Environment variables
```

## 🔐 Security Features

- **Multi-Factor Authentication (MFA)**
- **Role-Based Access Control (RBAC)**
- **JWT Token Authentication**
- **OAuth2 Integration**
- **SQL Injection Prevention**
- **XSS Protection**
- **CSRF Protection**
- **Rate Limiting**

## 🌐 Live Demo

- **Frontend**: https://quantashield.in
- **API**: https://api.quantashield.in

## 📊 Monitoring & Analytics

- Real-time threat intelligence dashboard
- Security incident tracking
- Compliance reporting
- Asset vulnerability assessments
- User activity monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Email: support@quantashield.in
- Documentation: [docs.quantashield.in](https://docs.quantashield.in)

---

**QuantaShield** - Securing the digital frontier, one threat at a time.

