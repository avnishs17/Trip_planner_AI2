# 🌍 AI Travel Planner

A production-ready AI-powered travel planning application built with **Flask** frontend and **FastAPI** backend. This application uses advanced AI agents to create personalized travel itineraries based on user preferences, budget, and requirements.

## 🏗️ Architecture

The application follows a modern microservices architecture:

- **Frontend**: Flask web application with responsive Bootstrap UI  
- **Backend**: FastAPI with LangGraph-based AI agents
- **AI Engine**: Multi-agent system using LangChain and various tools
- **Database**: File-based storage for travel plans
- **Deployment**: Containerized on Google Kubernetes Engine (GKE)

## ✨ Features

### 🎯 Core Features
- **AI-Powered Planning**: Advanced AI agents create personalized itineraries
- **Multi-Tool Integration**: Weather, currency, places, and expense calculation tools
- **Real-time Information**: Up-to-date data for informed planning
- **Budget Optimization**: Cost-effective travel plans within your budget
- **Responsive Design**: Mobile-friendly interface with single-page experience
- **Export Functionality**: Save plans to Markdown files

### 🛠️ Technical Features
- **Production-Ready**: Containerized with Docker and Kubernetes
- **Auto-Scaling**: Horizontal Pod Autoscaler based on CPU/Memory
- **Health Monitoring**: Built-in health check endpoints
- **Security**: Non-root containers, resource limits, secrets management
- **CI/CD**: Automated deployment with GitHub Actions

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Required API keys (see Configuration section)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd trip_planner_AI2
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   OPENWEATHERMAP_API_KEY=your_weather_api_key
   TAVILY_API_KEY=your_tavily_api_key
   EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
   FLASK_PORT=5000
   FLASK_DEBUG=True
   BACKEND_URL=http://localhost:8000
   ```

### Running the Application

1. **Start the FastAPI backend:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start the Flask frontend (in a new terminal):**
   ```bash
   python flask_app.py
   ```

### Access the Application

- **Frontend (Flask)**: http://localhost:5000
- **Backend API docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:5000/health

## 🔧 Required API Keys

You'll need to obtain the following API keys:

1. **Groq API Key**
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up and create an API key

2. **OpenAI API Key** (Optional)
   - Visit [OpenAI API](https://platform.openai.com/api-keys)
   - Create an API key

3. **OpenWeatherMap API Key**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account and get an API key

4. **Tavily API Key**
   - Visit [Tavily](https://tavily.com/)
   - Sign up and get an API key

5. **Exchange Rate API Key**
   - Visit [ExchangeRate-API](https://exchangerate-api.com/)
   - Sign up for a free account and get an API key

## 🚀 Production Deployment (GKE)

### Prerequisites

1. **Google Cloud Platform Account** with billing enabled
2. **GitHub Repository** with this code
3. **GKE Cluster** named `trip` in `us-central1` region
4. **Google Artifact Registry** repository named `trip` in `us-central1` region

### GCP Setup (Web Interface)

#### 1. Create GKE Cluster

1. **Go to GKE Console**
   - Visit: https://console.cloud.google.com/kubernetes/list
   - Select your project

2. **Create Cluster**
   - Click **"CREATE"** button
   - Choose **"GKE Standard"**

3. **Configure Cluster**
   - **Name**: `trip`
   - **Location type**: Zonal
   - **Zone**: `us-central1-c` (or any zone in us-central1)

4. **Configure Node Pool**
   - **Machine type**: `e2-medium`
   - **Boot disk size**: `20 GB`
   - **Number of nodes**: `3`

5. **Enable Features**
   - ✅ Enable autoscaling: Min `2`, Max `10`
   - ✅ Enable auto-repair
   - ✅ Enable auto-upgrade

6. **Create the cluster** (takes 5-10 minutes)

#### 2. Create Artifact Registry Repository

1. **Go to Artifact Registry Console**
   - Visit: https://console.cloud.google.com/artifacts
   - Select your project

2. **Create Repository**
   - Click **"CREATE REPOSITORY"**
   - **Name**: `trip`
   - **Format**: Docker
   - **Mode**: Standard
   - **Region**: `us-central1`
   - **Description**: `Trip Planner AI Docker images`

3. **Click "CREATE"**

#### 3. Create Service Account for GitHub Actions

1. **Go to IAM & Admin Console**
   - Visit: https://console.cloud.google.com/iam-admin/serviceaccounts
   - Select your project

2. **Create Service Account**
   - Click **"CREATE SERVICE ACCOUNT"**
   - **Service account name**: `github-actions-sa`
   - **Display name**: `GitHub Actions SA`
   - **Description**: `Service account for GitHub Actions`
   - Click **"CREATE AND CONTINUE"**

3. **Grant Roles**
   - Add these roles one by one:
     - `Kubernetes Engine Developer`
     - `Artifact Registry Writer`
     - `Kubernetes Engine Cluster Admin`
   - Click **"CONTINUE"** then **"DONE"**

4. **Create Key**
   - In the service accounts list, click on `github-actions-sa`
   - Go to **"KEYS"** tab
   - Click **"ADD KEY"** → **"Create new key"**
   - Choose **JSON** format
   - Click **"CREATE"** (downloads the JSON file)
   - **Save this JSON file content as `GCP_SA_KEY` GitHub secret**

### GitHub Secrets Configuration

#### Finding Your Project ID
1. Go to [GCP Console Dashboard](https://console.cloud.google.com/)
2. Your **Project ID** is shown in the project selector dropdown (top navigation)

#### Adding Secrets to GitHub
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** for each secret below:

| Secret Name | Description | How to Get Value |
|-------------|-------------|------------------|
| **`GCP_PROJECT_ID`** | Your Google Cloud Project ID | From GCP Console dashboard |
| **`GCP_SA_KEY`** | Service Account JSON Key | Copy entire contents of downloaded JSON file |
| **`GROQ_API_KEY`** | Groq API Key | Get from https://console.groq.com/ |
| **`OPENAI_API_KEY`** | OpenAI API Key (optional) | Get from https://platform.openai.com/api-keys |
| **`OPENWEATHERMAP_API_KEY`** | Weather API Key | Get from https://openweathermap.org/api |
| **`TAVILY_API_KEY`** | Search API Key | Get from https://tavily.com/ |
| **`EXCHANGE_RATE_API_KEY`** | Currency Exchange API Key | Get from https://exchangerate-api.com/ |

### Deployment Process

1. **Push to main branch** triggers GitHub Actions
2. **Build Docker image** (runs both Flask + FastAPI)
3. **Push to Artifact Registry** with commit SHA tag
4. **Deploy to GKE** with rolling update
5. **Verify deployment** and check service status

### Accessing the Deployed Application

After deployment, get the external IP:

```bash
kubectl get services -n trip-planner
```

The application will be available at the external IP on port 80.

## 🔍 Features

### Architecture
- **Single Container**: Both Flask frontend and FastAPI backend run in same pod
- **Auto-scaling**: 2-10 replicas based on CPU/Memory usage
- **Health Checks**: Automatic restart on failures
- **Security**: Non-root containers, resource limits, secrets management

### Monitoring
- Liveness probe on `/health` endpoint
- Readiness probe for traffic routing
- Resource monitoring and alerts

## 🛠️ Troubleshooting

### Check Pod Status
```bash
kubectl get pods -n trip-planner
kubectl describe pod <pod-name> -n trip-planner
```

### Check Logs
```bash
kubectl logs -f deployment/trip-planner -n trip-planner
```

### Common Issues
1. **Image pull errors**: Check Artifact Registry permissions
2. **Pod not starting**: Check secrets and environment variables
3. **Service not accessible**: Check LoadBalancer and firewall rules
4. **API errors**: Verify API keys in secrets