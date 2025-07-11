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

## 🚀 My Windows Development Setup

### 📋 What I Used

#### My System
- **Windows 11** (10.0.26100)
- **Python 3.11.7** (installed from python.org)
- **VS Code** with Python extension
- **Git for Windows**
- **PowerShell** as my terminal

### 🔧 How I Set Up My Environment

#### My Virtual Environment Setup

1. **I cloned the repository**
   ```powershell
   git clone <repository-url>
   cd trip_planner_AI2
   ```

2. **I created my virtual environment**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **I verified it was working**
   ```powershell
   where python
   # Output: D:\trip_planner_AI2\venv\Scripts\python.exe
   ```

### 📦 How I Installed Dependencies

1. **I installed all the required packages**
   ```powershell
   pip install -r requirements.txt
   ```

2. **I checked everything was installed correctly**
   ```powershell
   pip list | findstr "fastapi flask langchain groq"
   ```

### 🔑 How I Set Up My Environment

#### My .env File

I created a `.env` file in my project root with my actual API keys:

```env
# My API Keys
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
OPENWEATHERMAP_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
EXCHANGE_RATE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx

# My Flask Settings
FLASK_PORT=5000
FLASK_DEBUG=True
FLASK_ENV=development

# My FastAPI Settings
FASTAPI_PORT=8000
BACKEND_URL=http://localhost:8000

# My App Settings
OUTPUT_DIR=output
LOG_LEVEL=INFO
RELOAD=True
WORKERS=1
```

#### How I Got My API Keys

1. **Groq API Key** - I got this from [console.groq.com](https://console.groq.com/)
   - Signed up with my email
   - Went to API Keys section
   - Created a new key (free account gives good quota)

2. **OpenWeatherMap API Key** - From [openweathermap.org/api](https://openweathermap.org/api)
   - Free account gives 1000 calls/day
   - Found my key in the API keys section after signup

3. **Tavily API Key** - From [tavily.com](https://tavily.com/)
   - Free tier gives 1000 searches/month
   - Got the key from their API dashboard

4. **Exchange Rate API Key** - From [exchangerate-api.com](https://exchangerate-api.com/)
   - Free account gives 1500 requests/month
   - Key was available immediately after signup

### 🏃‍♂️ How I Run My Application

#### My Daily Development Process

I open two PowerShell windows and run these commands:

1. **PowerShell Window 1 - Backend**
   ```powershell
   # I activate my virtual environment
   venv\Scripts\activate

   # I start FastAPI backend with auto-reload
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info
   ```

2. **PowerShell Window 2 - Frontend**
   ```powershell
   # I activate my virtual environment
   venv\Scripts\activate

   # I start Flask frontend
   python flask_app.py
   ```


### 🌐 My Application URLs

After I start both services, I can access:

- **Main App**: http://localhost:5000 (this is where I create travel plans)
- **API Documentation**: http://localhost:8000/docs (interactive FastAPI docs)
- **Health Check**: http://localhost:5000/health (to verify Flask is running)
- **Backend Health**: http://localhost:8000/health (to verify FastAPI is running)

### 📁 My Project Layout

This is how my project is organized:

```
D:\trip_planner_AI2\
├── 📁 agent\                   # AI workflow logic
├── 📁 config\                  # Configuration files
├── 📁 exception\               # Error handling
├── 📁 logger\                  # Logging setup
├── 📁 output\                  # My generated travel plans (*.md files)
├── 📁 prompt_library\          # AI prompts I use
├── 📁 static\                  # CSS styling
├── 📁 templates\               # HTML templates
├── 📁 tools\                   # AI tools (weather, currency, etc.)
├── 📁 utils\                   # Helper functions
├── 📁 venv\                    # My virtual environment
├── 📄 flask_app.py            # Frontend server
├── 📄 main.py                 # Backend API server
├── 📄 requirements.txt        # Dependencies
├── 📄 .env                   # My API keys (I created this)
├── 📄 start_backend.bat      # My helper script
├── 📄 start_frontend.bat     # My helper script
└── 📄 README.md             # This documentation
```

### 🔧 How I Test

- I go to http://localhost:5000 and create test travel plans
- I check the generated files in my `output/` folder

### 🐛 Problems I've Encountered

#### Port Issues

When I get "port already in use" errors:
```powershell
# I find what's using my ports
netstat -ano | findstr :5000
netstat -ano | findstr :8000

# I kill the process if needed
taskkill /PID <PID> /F
```

#### API Key Problems

When I get API errors:
```powershell
# I check my .env file
type .env

# I verify my keys are loaded
python -c "import os; print(os.getenv('GROQ_API_KEY'))"
```

#### Import Errors

When I get module not found errors:
```powershell
# I reinstall everything
pip install --force-reinstall -r requirements.txt
```

#### Virtual Environment Issues

When my venv gets messed up:
```powershell
# I recreate it completely
deactivate
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### When Things Are Slow

- Sometimes my API keys hit rate limits
- I restart both services to clear memory
- I check my internet connection



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
   - **Zone**: `us-central1-a` (or any zone in us-central1)

4. **Networking**
   - **Tick DNS option**

5. **Create the cluster** (takes 5-10 minutes)

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
     - `Artifact Registry Administrator`

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

## 🔍 Production Features

### Architecture
- **Single Container**: Both Flask frontend and FastAPI backend run in same pod
- **Auto-scaling**: 2-10 replicas based on CPU/Memory usage
- **Health Checks**: Automatic restart on failures
- **Security**: Non-root containers, resource limits, secrets management

### Monitoring
- Liveness probe on `/health` endpoint
- Readiness probe for traffic routing
- Resource monitoring and alerts

## 🛠️ Production Troubleshooting

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