import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from collections import Counter
import os


class ETLProcessor:
    def __init__(self):
        # Database connection details
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_NAME = os.getenv("DB_NAME", "postgres")
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASS = os.getenv("DB_PASS", "password")

    @staticmethod
    def clean_df(df, remove):
        df.columns = df.columns.str.replace(remove, "")
        df = df.applymap(lambda x: x.replace(remove, "") if isinstance(x, str) else x)
        return df

    def derive_features(self):
        users_df = self.clean_df(pd.read_csv("data/users.csv"), "\t")
        experiments_df = self.clean_df(pd.read_csv("data/user_experiments.csv"), "\t")
        compounds_df = self.clean_df(pd.read_csv("data/compounds.csv"), "\t")

        # Derive total experiments a user ran
        total_experiments = experiments_df.groupby("user_id").size()

        # Derive average experiments amount overall
        avg_experiments = experiments_df.groupby("user_id").size().mean()

        # Derive total experiments across all users
        total_experiments_all_users = total_experiments.sum()

        # Derive average experiments per user
        experiments_pct = total_experiments / total_experiments_all_users

        # Derive user's most commonly experimented compound
        experiments_df["experiment_compound_ids"] = experiments_df[
            "experiment_compound_ids"
        ].str.split(";")
        user_compounds = experiments_df.explode("experiment_compound_ids")
        most_common_compound_id = user_compounds.groupby("user_id")[
            "experiment_compound_ids"
        ].apply(lambda x: Counter(x).most_common(1)[0][0])

        # Derive user's most commonly experimented compound name
        compounds_df["compound_id"] = compounds_df["compound_id"].astype(str)
        user_compounds["experiment_compound_ids"] = user_compounds[
            "experiment_compound_ids"
        ].astype(str)
        user_compounds = user_compounds.join(
            compounds_df.set_index("compound_id"),
            on="experiment_compound_ids",
            how="left",
        )
        most_common_compound_name = user_compounds.groupby("user_id")[
            "compound_name"
        ].apply(lambda x: Counter(x).most_common(1)[0][0])

        # Combine all data
        users_df.set_index("user_id", inplace=True)
        users_df["total_experiments"] = total_experiments
        users_df["avg_experiments"] = avg_experiments
        users_df["experiments_pct"] = experiments_pct
        users_df["most_common_compound_id"] = most_common_compound_id
        users_df["most_common_compound_name"] = most_common_compound_name

        return users_df

    async def etl(self):
        # Load CSV files
        # Process files to derive features
        # Upload processed data into a database
        features_df = self.derive_features()

        # Try to intialize db connection
        conn = None
        cursor = None
        message = ""
        try:
            # Establish a connection to the database
            conn = psycopg2.connect(
                dbname=self.DB_NAME,
                user=self.DB_USER,
                password=self.DB_PASS,
                host=self.DB_HOST,
            )
            cursor = conn.cursor()

            # Create the features table if it doesn't exist
            create_table_query = """
                CREATE TABLE IF NOT EXISTS features (
                    user_id INT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    signup_date DATE,
                    total_experiments INT,
                    avg_experiments FLOAT,
                    experiments_pct FLOAT,
                    most_common_compound_id INT,
                    most_common_compound_name TEXT
                );
                """
            cursor.execute(create_table_query)

            # Insert data into PostgreSQL table
            execute_values(
                cursor,
                "INSERT INTO features (user_id, name, email, signup_date, total_experiments, avg_experiments, experiments_pct, most_common_compound_id, most_common_compound_name) VALUES %s",
                list(features_df.itertuples(index=True, name=None)),
            )

            # Commit the transaction
            conn.commit()

            # Success message
            message = "successfully inserted into database"

        # Catch any database errors
        except psycopg2.Error as e:
            # If an error occurred, rollback the transaction
            if conn is not None:
                conn.rollback()

            # Error message
            message = f"a database error occurred:\n{e}"

        # In the end, ensure the connection and cursor are closed
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return message
