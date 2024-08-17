import streamlit as st
import requests
import pandas as pd

BASE_URL = "PUBLIC_URL"

st.title("AutoML Builder")

def train_model(file):
    files = {'file': file}
    response = requests.post(f"{BASE_URL}/train", files=files)
    return response.json()

def check_status(task_id):
    response = requests.get(f"{BASE_URL}/monitor/{task_id}")
    return response.json()

def make_prediction(task_id, file):
    data = {'task_id': task_id}
    files = {'file': file}
    response = requests.post(f"{BASE_URL}/predict", data=data, files=files)
    return response.json()

tab1, tab2, tab3 = st.tabs(["Train Model", "Monitor Training", "Make Predictions"])

with tab1:
    st.header("Train a New Model")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        if st.button("Train Model"):
            result = train_model(uploaded_file)
            st.write(result)

with tab2:
    st.header("Monitor Training Status")
    task_id = st.text_input("Enter Task ID")
    if st.button("Check Status"):
        status = check_status(task_id)
        st.write(status)

with tab3:
    st.header("Make Predictions")
    task_id = st.text_input("Enter Model ID")
    prediction_file = st.file_uploader("Choose a CSV file for prediction", type="csv")
    if prediction_file is not None:
        if st.button("Predict"):
            predictions = make_prediction(task_id, prediction_file)
            predictions_df = pd.DataFrame(predictions)
            st.write(predictions_df)
