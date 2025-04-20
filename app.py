from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_restx import Api, Resource, fields
import os
from config import config
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pandas as pd
import tensorflow as tf
from pyspark.sql import SparkSession
import logging
from datetime import datetime, timedelta
from marshmallow import Schema, fields as marshmallow_fields, validate
import uuid

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['default'])
config['default'].init_app(app)

# Initialize extensions
CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})
jwt = JWTManager(app)

# Initialize API documentation
api = Api(app, version='1.0', title='Healthcare Analytics API',
          description='API for healthcare data analytics and anomaly detection')

# Configure logging
logging.basicConfig(level=app.config['LOG_LEVEL'])
logger = logging.getLogger(__name__)

# Initialize Azure services
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=app.config['AZURE_KEY_VAULT_URI'], credential=credential)
cosmos_client = CosmosClient(app.config['AZURE_COSMOS_ENDPOINT'], credential=app.config['AZURE_COSMOS_KEY'])
database = cosmos_client.get_database_client("HealthcareDB")
container = database.get_container_client("PatientData")

# Initialize Spark
spark = SparkSession.builder.appName("HealthcareETL").getOrCreate()

# Schema definitions for request validation
class PatientDataSchema(Schema):
    patient_id = marshmallow_fields.String(required=True)
    age = marshmallow_fields.Integer(validate=validate.Range(min=0, max=120))
    disease = marshmallow_fields.String(required=True)
    timestamp = marshmallow_fields.DateTime(required=True)

# API Models for Swagger documentation
patient_model = api.model('Patient', {
    'patient_id': fields.String(required=True, description='Patient identifier'),
    'age': fields.Integer(required=True, description='Patient age'),
    'disease': fields.String(required=True, description='Diagnosed disease'),
    'timestamp': fields.DateTime(required=True, description='Record timestamp')
})

# Sample TensorFlow model for anomaly detection
def load_anomaly_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation="relu", input_shape=(10,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=['accuracy'])
    return model

anomaly_model = load_anomaly_model()

@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        """Check API health status"""
        return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}

@api.route('/auth/login')
class Login(Resource):
    @api.doc('login')
    @api.expect(api.model('Login', {
        'username': fields.String(required=True),
        'password': fields.String(required=True)
    }))
    def post(self):
        """User login and token generation"""
        data = request.get_json()
        # In a real application, verify credentials against a user database
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200

@api.route('/data/upload')
class DataUpload(Resource):
    @api.doc('upload_data', security='Bearer')
    @api.expect(api.model('FileUpload', {
        'file': fields.String(required=True, description='CSV file to upload')
    }))
    @jwt_required()
    def post(self):
        """Upload and process healthcare data"""
        try:
            if 'file' not in request.files:
                return {'error': 'No file provided'}, 400
            
            file = request.files['file']
            if not file.filename.endswith('.csv'):
                return {'error': 'Only CSV files are supported'}, 400
            
            # Save file temporarily
            filename = f"{uuid.uuid4()}.csv"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read and validate data
            df = pd.read_csv(filepath)
            schema = PatientDataSchema(many=True)
            try:
                validated_data = schema.load(df.to_dict('records'))
            except Exception as e:
                return {'error': f'Data validation failed: {str(e)}'}, 400
            
            # Process with Spark
            spark_df = spark.createDataFrame(df)
            spark_df = spark_df.dropna()
            
            # Store in Cosmos DB
            for row in spark_df.toPandas().to_dict('records'):
                container.upsert_item(row)
            
            # Clean up
            os.remove(filepath)
            
            logger.info(f"Successfully processed file: {file.filename}")
            return {'message': 'Data uploaded successfully', 'records': len(df)}, 200
        
        except Exception as e:
            logger.error(f"Error uploading data: {str(e)}")
            return {'error': str(e)}, 500

@api.route('/dashboard')
class Dashboard(Resource):
    @api.doc('get_dashboard', security='Bearer')
    @jwt_required()
    def get(self):
        """Get healthcare dashboard trends"""
        try:
            query = "SELECT c.disease, COUNT(c.id) as count FROM c GROUP BY c.disease"
            items = list(container.query_items(query, enable_cross_partition_query=True))
            return {'trends': items}, 200
        except Exception as e:
            logger.error(f"Error fetching dashboard trends: {str(e)}")
            return {'error': str(e)}, 500

@api.route('/analytics/anomalies')
class Anomalies(Resource):
    @api.doc('get_anomalies', security='Bearer')
    @jwt_required()
    def get(self):
        """Detect anomalies in recent healthcare data"""
        try:
            query = "SELECT * FROM c WHERE c.timestamp > @recent ORDER BY c.timestamp DESC"
            items = list(container.query_items(
                query=query,
                parameters=[{"name": "@recent", "value": (datetime.utcnow() - timedelta(days=7)).isoformat()}],
                enable_cross_partition_query=True
            ))
            
            df = pd.DataFrame(items)
            if not df.empty:
                features = df.select_dtypes(include=['float64', 'int64']).values
                predictions = anomaly_model.predict(features)
                anomalies = df[predictions > 0.5].to_dict('records')
            else:
                anomalies = []
            
            return {'anomalies': anomalies}, 200
        
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return {'error': str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=app.config['DEBUG'])