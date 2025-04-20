# Healthcare Data Analysis Platform
A powerful platform for diving into anonymized healthcare data to uncover trends, built with secure, scalable pipelines that grow with your needs.

## What It Does
- Spots unusual patterns in disease trends
- Offers interactive charts and visualizations
- Keeps data safe with HIPAA-compliant security
- Handles large datasets with robust ETL pipelines

## Tools & Tech
- **Backend**: Python with Flask for lightweight APIs
- **Frontend**: Vue.js for a smooth, dynamic interface
- **Data Processing**: Apache Spark for heavy lifting
- **AI**: TensorFlow for smart trend detection
- **Cloud**: Azure, using Kubernetes and Blob Storage
- **Database**: Azure Cosmos DB for flexible data storage

## How It’s Built
![Pipeline Diagram](docs/pipeline.png)
Data flows through a Spark-powered ETL pipeline, lands in Cosmos DB, and gets served up through Flask APIs for the frontend to display.

## Getting Started
1. Grab the code: `git clone https://github.com/yourusername/healthcare-data-platform`
2. Set up the backend: `pip install -r requirements.txt`
3. Set up the frontend: `npm install` in the client folder
4. Add your Azure credentials to a `.env` file
5. Kick off Spark jobs: `spark-submit spark_jobs/etl.py`
6. Launch the app: `flask run`
7. Check it out at: `http://localhost:8080`

## How to Use It
- Upload your datasets at `/data/upload`
- Explore trends on the `/dashboard`
- Dig into anomalies at `/analytics`

## Keeping It Secure
- Data’s locked down with Azure Key Vault encryption
- Role-based access control (RBAC) keeps things tight
- APIs run over HTTPS for safe communication

## Testing
Run `pytest tests/` to check the APIs and data pipelines.

## Deployment
Automated testing and deployment through Azure DevOps—see `.github/workflows/ci.yml` for details.

## What’s Next
- Let users ask questions in plain English
- Tune Spark jobs to crunch even bigger datasets

---
Built by Odon Dushime. Let’s connect on LinkedIn: www.linkedin.com/in/odon-dushime-276b9b271
