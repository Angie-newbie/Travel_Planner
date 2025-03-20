# Travel Planner API

## Overview
The Travel Planner API allows users to manage trips, expenses, and categories efficiently. The API is built with Flask, SQLAlchemy, and Marshmallow for data validation and serialization.

## Prerequisites
Ensure you have the following installed:
- Python (>= 3.8)
- PostgreSQL
- Flask & required dependencies (see `requirements.txt`)

## Setup Instructions

### 1. Clone the Repository
```sh
    git clone <your-repo-url>
    cd Travel_Planner
```

### 2. Create a Virtual Environment
```sh
    python -m venv .venv
    source .venv/bin/activate  # On Mac/Linux
    .venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```sh
    pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and configure your database settings:
```
DATABASE_URL=postgresql://username:password@localhost:5432/travel_planner_db
FLASK_APP=main.py
FLASK_ENV=development
```

### 5. Initialize the Database
Before running the API, you must initialize the database schema and seed it with sample data.

#### **Flush & Initialize the Database**
```sh
    flask db init
```
This will create the necessary database schema.

#### **Seed the Database with Sample Data**
```sh
    flask db seed
```
This step populates the database with sample users, trips, categories, and expenses.

### 6. Run the API
Start the Flask development server:
```sh
    flask run
```
The API should now be running at `http://127.0.0.1:5000/`

## API Endpoints

### **Expenses**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/expenses` | Retrieve all expenses |
| GET | `/expenses/<id>` | Retrieve a specific expense |
| POST | `/expenses` | Create a new expense |
| PUT/PATCH | `/expenses/<id>` | Update an expense |
| DELETE | `/expenses/<id>` | Delete an expense |

### **Trips**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/trips` | Retrieve all trips |
| GET | `/trips/<id>` | Retrieve a specific trip |
| POST | `/trips` | Create a new trip |
| PUT/PATCH | `/trips/<id>` | Update a trip |
| DELETE | `/trips/<id>` | Delete a trip |

### **Categories**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | Retrieve all categories |
| GET | `/categories/<id>` | Retrieve a specific category |
| POST | `/categories` | Create a new category |
| PUT/PATCH | `/categories/<id>` | Update a category |
| DELETE | `/categories/<id>` | Delete a category |

## Troubleshooting

### **Port 5000 Already in Use**
If you see an error stating `Address already in use`, stop the process using port 5000:
```sh
    lsof -i :5000  # Find the process using port 5000
    kill -9 <PID>  # Replace <PID> with the process ID
```

### **Database Issues**
If you encounter database errors, try resetting it:
```sh
    flask db init
    flask db seed
```

## License
This project is licensed under the MIT License.

