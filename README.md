# Healthcare Analytics API

A robust Flask-based API for healthcare data analytics and anomaly detection, featuring Azure integration, JWT authentication, and machine learning capabilities.

## Features

- **Secure Authentication**: JWT-based authentication with refresh tokens
- **Data Processing**: CSV file upload and processing with pandas and PySpark
- **Anomaly Detection**: TensorFlow-based anomaly detection in healthcare data
- **Dashboard Analytics**: Real-time healthcare trends and statistics
- **Azure Integration**: Cosmos DB and Key Vault integration
- **API Documentation**: Swagger/OpenAPI documentation
- **Input Validation**: Robust data validation using Marshmallow
- **Health Monitoring**: Health check endpoint for monitoring

## Prerequisites

- Python 3.8+
- Azure account with Cosmos DB and Key Vault
- Spark (for local development)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/healthcare-analytics.git
cd healthcare-analytics
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

The application uses the following environment variables:

- `FLASK_SECRET_KEY`: Secret key for Flask
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `AZURE_COSMOS_ENDPOINT`: Azure Cosmos DB endpoint
- `AZURE_COSMOS_KEY`: Azure Cosmos DB key
- `AZURE_KEY_VAULT_URI`: Azure Key Vault URI
- `CORS_ORIGINS`: Allowed CORS origins
- `LOG_LEVEL`: Logging level

## Running the Application

1. Start the Flask development server:

```bash
python app.py
```

2. Access the API documentation at:

```
http://localhost:8080/
```

## API Endpoints

### Authentication

- `POST /auth/login`: User login and token generation

### Data Management

- `POST /data/upload`: Upload and process healthcare data
- `GET /dashboard`: Get healthcare dashboard trends
- `GET /analytics/anomalies`: Detect anomalies in recent data

### System

- `GET /health`: Check API health status

## Security

- JWT-based authentication
- Role-based access control
- Input validation
- Secure file handling
- CORS protection

## Development

### Code Style

The project uses Black for code formatting and Flake8 for linting:

```bash
black .
flake8
```

### Testing

Run tests using pytest:

```bash
pytest
```

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Configure proper CORS origins
3. Set up proper logging
4. Use a production-grade WSGI server (e.g., Gunicorn)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built by Odon Dushime. Let's connect on LinkedIn: www.linkedin.com/in/odon-dushime-276b9b271
