This project fetches weather information from the OpenWeather API using an API key, stores the data in a database, and predicts future weather using a Linear Regression model with the latest dataset from Kaggle and stored data in database

Features: 
  * Fetch current weather data for a specific city using the OpenWeather API.
  * Store and retrieve weather data from a database.
  * Predict future weather conditions using a Linear Regression model.
    
To Execute following these Steps:

    * # Create a virtual environment named 'project'
      python -m venv project
    * # Activate the virtual environment
      project\Scripts\activate
    * # Install Django in the virtual environment
      pip install django
    * # Create a new Django project named 'weather_prediction'
      django-admin startproject weather_prediction
    * # Navigate into the project directory
      cd weather_prediction
    * python manage.py startapp weather
            * define views.py---> Once the frontend functions are implemented, the server should respond appropriately based on the defined views.   
    * Create a folder named Templates--> This folder contains HTML pages for client-server interactions, with each page performing its specific function as defined by the backend logic
    * To the Store the user input; Create your database schema in model.py and execute
    * python manage.py makemigrations
      python manage.py migrate

Handling Package Errors:
* If any package errors occur during installation, kindly install the required packages using the pip command. 
For example: pip install <package>

  


