# 🧠 Cognitive Assessment API

A RESTful Flask-based API for analyzing journal entries using a LIWC-like dictionary. The system allows users to register, submit entries, and receive psychological category scores based on their text.

## Features

- User registration and JWT-based login
- Journal submission with LIWC-style scoring
- Secure endpoints with token-based authentication
- Modular code structure (models, routes, services, tests)
- 100% test coverage with `pytest`

## Project Structure

project-root/
│
├── app/
│   ├── models/       # SQLAlchemy models (User, Journal)
│   ├── routes/       # API endpoint definitions
│   ├── services/     # Business logic (e.g., LIWC scoring)
│   ├── tests/        # Unit tests
│   ├── utils/        # Constants and helpers
│   └── __init__.py   # App factory
│
├── liwc_dictionary.json     # LIWC-like dictionary
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container setup (optional)
├── README.md                # Project documentation
└── pytest.ini               # Pytest config

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.10+
- `virtualenv` (recommended)

### 🔌 Installation

# Clone the repo
git clone https://github.com/yourusername/cognitive-api.git
cd cognitive-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

## 🧪 Running the App

# Initialize DB and run locally
python -m flask --app app run --debug


## 🧠 API Endpoints

### 🔐 Auth

- `POST /users` — Register a user
- `POST /login` — Login and get JWT token

### 📓 Journals

- `POST /journals` — Submit journal (JWT required)
- `GET /journals/<journal_id>/score` — Get score (JWT required)


## Running Tests

### With coverage:

# Ensure app/ is in PYTHONPATH
PYTHONPATH=. pytest app/tests/ --disable-warnings --tb=short

Or add a `pytest.ini` and simply run: pytest

## Docker File Usage Instructions

### Build the Docker image using below command

docker build -t cognitive-api .

### Run the container using below command

docker run -d -p 5000:5000 --name cognitive-api cognitive-api
