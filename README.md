# Backend Engineering Take-Home Challenge

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

4. A brief README explaining how to build and run your application, and how to trigger the ETL process.

    1. Create .env file containing db credentials as contents in root like this:

    DB_USER=postgres
    DB_PASS=password
    DB_NAME=postgres
    DB_HOST=db
    POSTGRES_PASSWORD=password

    2. Build and run docker, start Flask server: docker-compose up --build
    3. Trigger ETL from API endpoint GET http://127.0.0.1:5000/trigger_etl
        - access from browser http://127.0.0.1:5000/trigger_etl
        -   - docker exec -it <web_container_id> /bin/bash
            - curl http://127.0.0.1:5000/trigger_etl
    4. Query db to check insert was succesfull
        - docker exec -it <db_container_id> /bin/bash
        - psql -h localhost -U [username] -d [database]
        - SELECT * FROM features;

        Successful output example:
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

Please also provide a script that builds, and runs the docker container. 
You should also provide a script that scaffolds how a user can run the ETL process. This can be `curl` or something else.
Finally, provide a script that queries the database and showcases that it has been populated with the desired features.


## Evaluation
Your solution will be evaluated on the following criteria:

Code quality and organization.
Proper use of Python and Docker.
Successful execution of the ETL process.
Accuracy of the derived features.
