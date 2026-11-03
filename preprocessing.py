import pandas as pd

from database import connection

# print(connection.is_connected())

query = "select * from customers"
df = pd.read_sql(query, connection)

df = pd.get_dummies(
    df,
    columns=["plan","contract_type","city"],
    drop_first=True
)
print(df)


