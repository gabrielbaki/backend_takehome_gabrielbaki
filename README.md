# Backend Engineering Take-Home Challenge

## How to run the code
1. Create .env file in root containing db credentials as contents in root like this (add it to .gitignore for security):

    DB_USER=postgres  
    DB_PASS=password  
    DB_NAME=postgres  
    DB_HOST=db  
    POSTGRES_PASSWORD=password

2. Build and run docker, start Flask server: docker-compose up --build

3. Trigger ETL from API endpoint GET http://127.0.0.1:5000/trigger_etl
        a. access from browser http://127.0.0.1:5000/trigger_etl
        b. In root directory:  
            - docker exec -it <web_container_id> /bin/bash
            - curl http://127.0.0.1:5000/trigger_etl

4. Query db to check insert was succesfull
        - docker exec -it <db_container_id> /bin/bash
        - psql -h localhost -U [username] -d [database]
        - SELECT * FROM features;

        Example of successful terminal output:  
         user_id | name  |       email       | signup_date | total_experiments | avg_experiments | experiments_pct | most_common_compound_id | most_common_compound_name 
---------+-------+-------------------+-------------+-------------------+-----------------+-----------------+------------------------+---------------------------
 1 | Alice | alice@example.com | 2023-01-01 | 2 | 1.1 | 0.181818181818182 | 2 | Compound B
 2 | Bob | bob@example.com | 2023-02-01 | 1 | 1.1 | 0.0909090909090909 | 1 | Compound A
 3 | Carol | carol@example.com | 2023-03-01 | 1 | 1.1 | 0.0909090909090909 | 2 | Compound B
 4 | Dave | dave@example.com | 2023-04-01 | 1 | 1.1 | 0.0909090909090909 | 1 | Compound A
 5 | Eve | eve@example.com | 2023-05-01 | 1 | 1.1 | 0.0909090909090909 | 2 | Compound B
 6 | Frank | frank@example.com | 2023-06-01 | 1 | 1.1 | 0.0909090909090909 | 1 | Compound A
 7 | Grace | grace@example.com | 2023-07-01 | 1 | 1.1 | 0.0909090909090909 | 2 | Compound B
 8 | Heidi | heidi@example.com

## ETL API Documentation
The ETL API has been designed to execute an Extract-Transform-Load (ETL) process, reading data from CSV files, deriving and processing data, and then loading the data into a PostgreSQL database. The ETL process is triggered via a HTTP GET request. This documentation provides an overview of the available endpoints and the functionality of the ETL processor.

### API Endpoint  
Endpoint: /trigger_etl  
Method: GET  
This endpoint runs from `app.py` triggers the ETL process. It does not require any parameters or body content.  

- Request:  No parameters or body content are required.  

- Response:  The response to this GET request will be a JSON object containing a status message and the result of the ETL process.

Example:
{
  "message": "ETL process started",
  "result": "successfully inserted into database"
}

### ETLProcessor Class  
The ETLProcessor class in `etl_processor.py` is responsible for the main functionality of the ETL process. The class contains methods for cleaning the data (clean_df), deriving new features (derive_features), and executing the overall ETL process (etl).

- clean_df(df, remove):  This method takes in a dataframe and a string to be removed from all column names and cell values, and returns the cleaned dataframe.

- derive_features():  This method reads data from three CSV files ('users.csv', 'user_experiments.csv', 'compounds.csv'), derives new features, and returns a dataframe with the derived features for each user which includes columns from user csv, total experiments a user ran, experiment percentage for that user compared to total, average experiments amount per user, user's most commonly experimented compound id, and it's name.

- etl():  This is an asynchronous method that conducts the ETL process. It calls derive_features to get the data and then inserts the data into a PostgreSQL database. The connection details for the database are fetched from environment variables. If the connection is successful, a table named 'features' is created if it does not already exist, and the data is inserted into the table. If there is any error during the process, the error message is returned. After the process completes, the connection to the database is closed. This method returns a message indicating whether the data was successfully inserted into the database or if an error occurred.

### Docker Environment

- `Dockerfile`: The Dockerfile for the Python application. It begins with a Python 3.7 base image. It sets the working directory to /app. The requirements.txt file is copied into the Docker image and pip install is run to install these dependencies. Then all the files from the current directory are copied into the Docker image. Finally, CMD sets the default command to run when a container is run from this image, which in this case is python app.py.

- `Dockerfile-db`: This is the Dockerfile for the PostgreSQL database. It starts with a PostgreSQL 11 base image. It declares an argument POSTGRES_PASSWORD_ARG and then uses this argument to set the environment variable POSTGRES_PASSWORD which is used by the PostgreSQL image to set the database password.

- `docker-compose.yml`: In the docker-compose file, there are two services declared: web and db. The web service is built using the Dockerfile in the current directory, binds the host's port 5000 to the container's port 5000, creates a volume that maps the current directory on the host to /app in the container, and sets environment variables for database connection. It also specifies that the web service depends on the db service. The db service is built using Dockerfile-db in the current directory, exposes port 5432 (PostgreSQL's default port), sets the POSTGRES_PASSWORD environment variable, and uses a named volume postgres_data for persisting the database data. A volume postgres_data is declared at the bottom which is used by the db service.

- `requirements.txt`: Outlines the Python library dependencies needed for the project. The libraries in use here are:

### Input Data
CSV files in the `data`  directory:

- `users.csv`: Contains user data with the following columns: `user_id`, `name`, `email`,`signup_date`.

- `user_experiments.csv`: Contains experiment data with the following columns: `experiment_id`, `user_id`, `experiment_compound_ids`, `experiment_run_time`. The `experiment_compound_ids` column contains a semicolon-separated list of compound IDs.


- `compounds.csv`: Contains compound data with the following columns: `compound_id`, `compound_name`, `compound_structure`.
