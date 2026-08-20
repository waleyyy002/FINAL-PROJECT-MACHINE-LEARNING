from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib


# ==========================================
# LOAD MODEL
# ==========================================

churn_model = joblib.load(
    "customer_churn_prediction.pkl"
)

model = churn_model["model"]
scaler = churn_model["scaler"]
label_encoders = churn_model["label_encoders"]
# feature names may be saved in the checkpoint under 'feature_names'.
# If not present, try to infer from the fitted estimator or scaler.
if "feature_names" in churn_model:
    feature_names = churn_model["feature_names"]
else:
    feature_names = None
    if hasattr(model, "feature_names_in_"):
        feature_names = list(model.feature_names_in_)
    elif hasattr(scaler, "feature_names_in_"):
        feature_names = list(scaler.feature_names_in_)

    if feature_names is None:
        raise KeyError(
            "'feature_names' not found in checkpoint and could not infer from model/scaler."
        )


# ==========================================
# CREATE FASTAPI APP
# ==========================================

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting whether a customer will churn.",
    version="1.0.0"
)


# ==========================================
# INPUT DATA MODEL
# ==========================================

class CustomerData(BaseModel):

    Gender: str
    Senior_Citizen: str
    Partner: str
    Dependents: str
    Tenure_Months: int
    Phone_Service: str
    Multiple_Lines: str
    Internet_Service: str
    Online_Security: str
    Online_Backup: str
    Device_Protection: str
    Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Monthly_Charges: float
    Total_Charges: float
    CLTV: int


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Customer Churn Prediction API",
        "status": "running",
        "docs": "/docs"
    }


# ==========================================
# HEALTH ENDPOINT
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True
    }


# ==========================================
# PREDICTION ENDPOINT
# ==========================================

@app.post("/predict")
def predict(data: CustomerData):

    # Convert input to dictionary
    input_data = data.model_dump()

    # Convert underscores back to original column names
    input_data = {
        "Gender": input_data["Gender"],
        "Senior Citizen": input_data["Senior_Citizen"],
        "Partner": input_data["Partner"],
        "Dependents": input_data["Dependents"],
        "Tenure Months": input_data["Tenure_Months"],
        "Phone Service": input_data["Phone_Service"],
        "Multiple Lines": input_data["Multiple_Lines"],
        "Internet Service": input_data["Internet_Service"],
        "Online Security": input_data["Online_Security"],
        "Online Backup": input_data["Online_Backup"],
        "Device Protection": input_data["Device_Protection"],
        "Tech Support": input_data["Tech_Support"],
        "Streaming TV": input_data["Streaming_TV"],
        "Streaming Movies": input_data["Streaming_Movies"],
        "Contract": input_data["Contract"],
        "Paperless Billing": input_data["Paperless_Billing"],
        "Payment Method": input_data["Payment_Method"],
        "Monthly Charges": input_data["Monthly_Charges"],
        "Total Charges": input_data["Total_Charges"],
        "CLTV": input_data["CLTV"]
    }

    # Create DataFrame
    input_df = pd.DataFrame([input_data])

    # Label encode categorical columns
    for column, encoder in label_encoders.items():

        if column in input_df.columns:

            input_df[column] = encoder.transform(
                input_df[column].astype(str)
            )

    # Make sure columns are in the same order
    input_df = input_df[feature_names]

    # Standardize
    input_scaled = scaler.transform(input_df)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    # Probability
    probability = model.predict_proba(
        input_scaled
    )[0][1]

    # Convert result
    if prediction == 1:
        result = "Churn"
    else:
        result = "No Churn"

    return {
        "prediction": result,
        "churn_probability": round(
            float(probability),
            4
        )
    }