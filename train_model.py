from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

from preprocessing import df

    
x = df.drop(["churn", "customer_id", "name"], axis=1)  #customer information
y = df["churn"]   #actual churn

joblib.dump(list(x.columns), "model_columns.pkl")

x_train,x_test,y_train,y_test = train_test_split(
        x,
        y,
        test_size= 0.2,
        random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(x_train,y_train)

print( "successfully trained")


y_predict = model.predict(x_test)

accuracy = accuracy_score(y_test, y_predict)   #actual ans, model ans

print("Accuracy:", accuracy)


print("Accuracy:", accuracy)

import joblib
joblib.dump(model, "churn_model.pkl")