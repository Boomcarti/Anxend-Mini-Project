# Anxend Interview Mini Project

## Overview
This Flask web application allows users to add and view schools in their town. It features a form for adding schools, including their name, address, and town, and displays a list of schools filtered by the selected town. The application uses Flask, WTForms for form handling, Flask-Caching for caching queries, and EdgeDB as the database backend.

## Features
- **Add School Form**: Users can submit details about a school, including its name, address, and town.
- **Dynamic Town Selection**: Users can select their town from a predefined list (Cape Town, London, New York) using interactive images. The list of schools updates to show only those in the selected town.
- **Caching**: School lists are cached to improve performance. The cache is invalidated and updated upon adding a new school.


# Setting Up the Database

1. Install EdgeDB from [the official site](https://edgedb.com/download).
2. Create a new database using EdgeDB CLI: `edgedb database create mydatabase`.
3. Apply schema migrations: Navigate to the `dbschema/` directory and run `edgedb migrate`.

# Configuring the Application

1. Install required Python packages: `pip install -r requirements.txt`.
2. Set up the database connection in `app.py` (if needed): Modify the `edgedb.create_client()` call to include your database credentials.
3. Run the application: `flask run` or `python app.py`.

Ensure you have set the `FLASK_APP` environment variable to `app.py` and optionally `FLASK_ENV` to `development` for development purposes.




## Setup and Installation

1. **Clone the Repository**: Clone this repository to your local machine.

git clone <repository-url>


2. **Create a Virtual Environment** (optional but recommended):

python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate



3. **Install Dependencies**:

pip install -r requirements.txt


4. **Configure EdgeDB**: Ensure that EdgeDB is installed and properly configured on your system. You may need to adjust the `edgedb.create_client()` call in the application to connect to your EdgeDB instance correctly.

5. **Run the Application**:


python app.py


The application will be accessible at `http://127.0.0.1:5000/`.

## Usage

- Navigate to the application URL in your web browser.
- Use the form to add a new school by entering its name, address, and town.
- Click on one of the town images to filter the list of schools by that town.
- The application will display schools based on the selected town.

## Caching Strategy

The application uses Flask-Caching with a simple cache to store the list of schools for each town. This cache is set to expire every 300 seconds (5 minutes) to ensure that the data remains relatively up-to-date without frequent database queries. When a new school is added, the cache for that particular town is invalidated to include the new entry in subsequent queries.

## Technical Details

- **Flask**: A micro web framework written in Python.
- **WTForms**: A flexible forms validation and rendering library for Python web development.
- **Flask-Caching**: Adds caching support to your Flask application.
- **EdgeDB**: A next-generation object-relational database that provides a rich query language and schema migration system.

