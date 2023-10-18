# Import the EvaDB package
import evadb

# Connect to EvaDB and get a database cursor for running queries
cursor = evadb.connect().cursor()

# List all the built-in functions in EvaDB
print(cursor.query("SHOW FUNCTIONS;").df())

# Create evadb database 
params = {
    "user": "eva",
    "password": "password",
    "host": "localhost",
    "port": "5432",
    "database": "evadb",
}
query = f"CREATE DATABASE postgres_data WITH ENGINE = 'postgres', PARAMETERS = {params};"
cursor.query(query).df()

# Build table
cursor.query("""
  USE postgres_data {
    CREATE TABLE IF NOT EXISTS creditcard_fraud (
      merchant_id VARCHAR(64),
      avg_amount FLOAT,
      transaction_amount FLOAT,
      is_declined INTEGER,
      total_declines INTEGER,
      is_foreign INTEGER,
      is_high_risk_country INTEGER,
      daily_chargeback_avg_amt FLOAT,
      six_month_avg_chbk_amt FLOAT,
      six_month_chbk_freq INTEGER,
      is_fraudulent INTEGER
    )
  }
""").df()

cursor.query("""
  USE postgres_data {
    COPY creditcard_fraud
    FROM '/Users/shuchen/Projects/evadb_fraud_detection/creditcard_fraud.csv'
    DELIMITER ',' CSV HEADER
  }
""").df()

# Quick view of data 
print (cursor.query("SELECT * FROM postgres_data.creditcard_fraud LIMIT 5").df())

# Quick analysis of data
print(cursor.query("""
  SELECT AVG(avg_amount), AVG(six_month_avg_chbk_amt)
  FROM postgres_data.creditcard_fraud
  WHERE is_fraudulent = 0;
"""
).df())
