import os
import joblib
import pandas as pd

import logging
from logging.handlers import RotatingFileHandler

# Ensure the 'logs' directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a rotating file handler
log_file = 'logs/application.log'
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)  # 5 MB per file, keep 5 backups
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load the trained Prophet model
model_path = 'utilities/helpers/accident/src/models/prophet_model.pkl'
if not os.path.exists(model_path):
    logger.error(f"Model file not found at {model_path}")
    raise FileNotFoundError(f"Model file not found at {model_path}")

logger.info(f"Loading model from {model_path}")
best_model = joblib.load(model_path)
logger.info("Model loaded successfully")


def main(year: int, month: int):
    logger.info(f"Received request for prediction: year={year}, month={month}")
    # Create a DataFrame for the requested date (Prophet requires a DataFrame)
    try:
        input_date = pd.to_datetime(f"{year}-{month}-01")
        future_df = pd.DataFrame({'ds': [input_date]})
        logger.info(f"Created future DataFrame for prediction: {future_df}")
    except Exception as e:
        logger.error(f"Error creating future DataFrame: {e}")
        raise

    # Make prediction
    try:
        forecast = best_model.predict(future_df)
        prediction_value = forecast['yhat'].iloc[0]
        logger.info(f"Prediction successful: {prediction_value}")
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise

    # Return the prediction as a dictionary
    result = {"prediction": prediction_value}
    logger.info(f"Returning prediction: {result}")
    return result
