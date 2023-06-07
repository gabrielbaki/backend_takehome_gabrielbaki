# Backend Engineering Take-Home Challenge

### How to run the code
1. Create .env file containing db credentials as contents in root like this:

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

        Successful terminal output example:  
        user_id | name  |       email       | signup_date | total_experim
ents | avg_experiments |  experiments_pct   | most_common_compound
_id | most_common_compound_name 
---------+-------+-------------------+-------------+--------------
-----+-----------------+--------------------+---------------------
----+---------------------------
       1 | Alice | alice@example.com | 2023-01-01  |              
   2 |             1.1 |  0.181818181818182 |                     
  2 | Compound B
       2 | Bob   | bob@example.com   | 2023-02-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  1 | Compound A
       3 | Carol | carol@example.com | 2023-03-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  2 | Compound B
       4 | Dave  | dave@example.com  | 2023-04-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  1 | Compound A
       5 | Eve   | eve@example.com   | 2023-05-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  2 | Compound B
       6 | Frank | frank@example.com | 2023-06-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  1 | Compound A
       7 | Grace | grace@example.com | 2023-07-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  2 | Compound B
       8 | Heidi | heidi@example.com | 2023-08-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  1 | Compound A
       9 | Ivan  | ivan@example.com  | 2023-09-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  2 | Compound B
      10 | Judy  | judy@example.com  | 2023-10-01  |              
   1 |             1.1 | 0.0909090909090909 |                     
  1 | Compound A

note: some deliverables description are in the "Deliverables" section.

### ETL API Documentation
The ETL API has been designed to execute an Extract-Transform-Load (ETL) process, reading data from CSV files, deriving and processing data, and then loading the data into a PostgreSQL database. The ETL process is triggered via a HTTP GET request. This documentation provides an overview of the available endpoints and the functionality of the ETL processor.

API Endpoint  
Endpoint: /trigger_etl  
Method: GET  
This endpoint triggers the ETL process. It does not require any parameters or body content.  

Request  
No parameters or body content are required.  

Response  
The response to this GET request will be a JSON object containing a status message and the result of the ETL process.

Example:

{
  "message": "ETL process started",
  "result": "successfully inserted into database"
}

ETLProcessor Class  
The ETLProcessor class is responsible for the main functionality of the ETL process. The class contains methods for cleaning the data (clean_df), deriving new features (derive_features), and executing the overall ETL process (etl).

clean_df(df, remove)  
This method takes in a dataframe and a string to be removed from all column names and cell values, and returns the cleaned dataframe.

derive_features()  
This method reads data from three CSV files ('users.csv', 'user_experiments.csv', 'compounds.csv'), derives new features, and returns a dataframe with the derived features for each user which includes columns from user csv, total experiments a user ran, experiment percentage for that user compared to total, average experiments amount per user, user's most commonly experimented compoun id, and it's name.

etl()  
This is an asynchronous method that conducts the ETL process. It calls derive_features to get the data and then inserts the data into a PostgreSQL database. The connection details for the database are fetched from environment variables. If the connection is successful, a table named 'features' is created if it does not already exist, and the data is inserted into the table. If there is any error during the process, the error message is returned. After the process completes, the connection to the database is closed.

This method returns a message indicating whether the data was successfully inserted into the database or if an error occurred.

## Deliverables
Please provide the following in a GITHUB REPOSITORY.

1. A Dockerfile that sets up the environment for your application.

- docker-compose.yml
- Dockerfile
- Dockerfile-db

2. A requirements.txt file with all the Python dependencies.

- requirements.txt

3. A Python script that sets up the API and the ETL process.

- app.py
- etl_processor.py

4. A brief README explaining how to build and run your application, and how to trigger the ETL process.

Please also provide a script that builds, and runs the docker container. 
You should also provide a script that scaffolds how a user can run the ETL process. This can be `curl` or something else.
Finally, provide a script that queries the database and showcases that it has been populated with the desired features.

note: all these points are adressed above in "How to run the code" section and added below the points in the "Deliverables" section

### Introduction
In this challenge, you will be tasked with creating a simple ETL pipeline that can be triggered via an API call. You will be provided with a set of CSV files that you will need to process, derive some features from, and then upload into a database table.

### Requirements
- Python 3.7+
- Docker
- PostgreSQL

### Challenge
1.  Create a Dockerized application that can be started with a single `docker run` command.

2. The application should expose an API endpoint that triggers an ETL process.

3. The ETL process should:
- Load CSV files from the given data directory.
 - Process these files to derive some simple features.
 - Upload the processed data into a **postgres** table.

4.  The application should be built using Python and any tooling you like for coordinating the workflow and fronting the api server

### Data
You will find three CSV files in the `data`  directory:

- `users.csv`: Contains user data with the following columns: `user_id`, `name`, `email`,`signup_date`.

- `user_experiments.csv`: Contains experiment data with the following columns: `experiment_id`, `user_id`, `experiment_compound_ids`, `experiment_run_time`. The `experiment_compound_ids` column contains a semicolon-separated list of compound IDs.


- `compounds.csv`: Contains compound data with the following columns: `compound_id`, `compound_name`, `compound_structure`.

## Feature Derivation
From the provided CSV files, derive the following features:

1. Total experiments a user ran.
2. Average experiments amount per user.
3. User's most commonly experimented compound.

## Evaluation
Your solution will be evaluated on the following criteria:

Code quality and organization.
Proper use of Python and Docker.
Successful execution of the ETL process.
Accuracy of the derived features.
