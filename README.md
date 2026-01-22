# Weather & Bikes Dashboard

A dashboard that analyzes and predicts bike availability based on weather conditions. This project combines real-time data from Citi Bike NYC and weather API to build models and provide visualizations. The dashboard is available at http://164.92.170.247:8050/.

## Features

- Real-time data collection from Citi Bike and weather API
- Machine learning model for bike availability prediction
- Interactive dashboard with visualizations
- Data pipeline with ETL processes
- Docker containerization
- Data version control with DVC

## Project Architecture
**Scripts**
- Script used for scheduling data collection
- Scripts for Docker setup

**ETL (src/etl/)**
- Handles data collection from external APIs (Citi Bikes, Open-Meteo)
- Transforms raw data into structured formats
- Loads data into database

**Database (src/db/)**
- Initializes and manages the database schema
- Stores historical data for analysis and model training

**Model (src/model/)**
- Implements machine learning model (RandomForestRegressor)
- Provides prediction functionality
- Handles feature engineering and data preparation

**UI (src/ui/)**
- Interactive web dashboard
- Plotly visualizations for data exploration
- Model predictions 
- Data integration from ETL pipelines

## Tech Stack

- **Language**: Python 3.11
- **Machine Learning**: Scikit-learn
- **Data Processing**: Pandas, NumPy, Dash
- **Visualization**: Plotly,
- **Data APIs**: Open-Meteo (weather), CityBikes (bike data)
- **Data Versioning**: DVC (Data Version Control)
- **Database**: PostgreSQL (psycopg2)
- **Container**: Docker

## Setup

### Required:

- Python 3.11 
- pip
- Docker
- DVC

### 1. Clone Repository

```bash
git clone <repository-url>
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Needed Packages

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables to Connect to the Database

```bash
nano .env
```

### 6. DVC

```bash
dvc pull
```

### Run Dashboard Locally

```bash
python -m src.ui.plots_ui
```

The dashboard is also available at http://164.92.170.247:8050/


## Data Pipeline

1. **Data Collection**: ETL modules fetch real-time bike availability and weather data
2. **Data Transformation**: Raw data is cleaned, and filtered
3. **Data Loading**: Processed data is stored in database
4. **Model Training**: ML model trained on historical data
5. **Predictions**: Model makes predictions based on current weather conditions
6. **Visualization**: Results displayed in dashboard

## Model Details

- **Algorithm**: Random Forest Regressor
- **Target Variable**: Percentage of used bikes
- Model saved as `model.pkl` and tracked with DVC

## Data Sources

- **Bike Data**: [CityBikes API](https://api.citybik.es/)
- **Weather Data**: [Open-Meteo API](https://open-meteo.com/)
