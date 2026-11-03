import pandas as pd
from database import connections

connection = connections()

print("Database connected")

query = "SELECT * FROM customers"

df = pd.read_sql(query, connection)

print(df)

print(df.shape)

print(df.columns)

df.info()

print(df.isnull().sum())

print(df["churn"].value_counts())

connection.close()


