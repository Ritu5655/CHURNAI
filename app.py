
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model and column names
model = joblib.load("churn_model.pkl")
model_columns = joblib.load("model_columns.pkl")

# app.secret_key = "kush"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Customer table
class user(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    plan = db.Column(db.String(20), nullable=False)
    monthly_charge = db.Column(db.Float, nullable=False)
    tenure_months = db.Column(db.Integer, nullable=False)
    contract_type = db.Column(db.String(20), nullable=False)
    churn = db.Column(db.Integer, nullable=False)


# Create database table and check database
with app.app_context():
    db.create_all()
    print("Database location:", db.engine.url.database)
    print("Customers in database:", user.query.count())


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# About section
@app.route("/about")
def about():
    return render_template("index.html")


# Prediction page
@app.route("/predict")
def predict():
    return render_template("index.html")

#contact
@app.route("/contact")
def contact():
   return render_template("contact.html")

# Add customer and predict churn
@app.route("/add", methods=["POST"])
def add_customer():
    try:
        customer_id = int(request.form.get("customer_id"))
        name = request.form.get("name")
        age = int(request.form.get("age"))
        city = request.form.get("city")
        plan = request.form.get("plan")
        monthly_charge = float(request.form.get("monthly_charge"))
        tenure_months = int(request.form.get("tenure_months"))
        contract_type = request.form.get("contract_type")

        # Prepare customer data
        customer_data = pd.DataFrame([{
            "age": age,
            "city": city,
            "plan": plan,
            "monthly_charge": monthly_charge,
            "tenure_months": tenure_months,
            "contract_type": contract_type
        }])

        # Convert categorical values into dummy columns
        customer_data = pd.get_dummies(
            customer_data,
            columns=["plan", "contract_type", "city"]
        )

        # Match training columns
        customer_data = customer_data.reindex(
            columns=model_columns,
            fill_value=0
        )

        # Predict churn
        prediction = int(model.predict(customer_data)[0])

        # Save customer to database
        new_customer = user(
            customer_id=customer_id,
            name=name,
            age=age,
            city=city,
            plan=plan,
            monthly_charge=monthly_charge,
            tenure_months=tenure_months,
            contract_type=contract_type,
            churn=prediction
        )

        db.session.add(new_customer)
        db.session.commit()

        print("Customer saved successfully!")
        print("Total customers:", user.query.count())

        if prediction == 1:
         result = "Churn"
        else:
         result = "No Churn"

        return render_template(
            "index.html",
            prediction=result,
            customer_name=name
        )

    except Exception as e:
        db.session.rollback()
        return f"Error: {e}", 400


if __name__ == "__main__":
    app.run(debug=True)
