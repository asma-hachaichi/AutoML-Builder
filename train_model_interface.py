import streamlit as st
import requests
import pandas as pd

st.title('H2O Model Trainer and Predictor')

st.header('Train Model')
uploaded_train_file = st.file_uploader("Choose a CSV file for training", type="csv", key='train')

if st.button('Train Model') and uploaded_train_file is not None:
    train_df = pd.read_csv(uploaded_train_file)
    train_csv_data = train_df.to_csv(index=False)

    response = requests.post(
        url="https://98db-34-106-63-144.ngrok-free.app/train",
        files={'file': ('train.csv', train_csv_data)}
    )

    if response.status_code == 200:
        train_result = response.json()
        st.success('Model Trained Successfully!')
        st.json(train_result)
        modelpath = train_result['modelpath']
        st.session_state['modelpath'] = modelpath
    else:
        st.error('Training failed')
        st.write(response.text)

if 'modelpath' in st.session_state:
    st.header('Predict with Model')
    st.write(f"Model Path: {st.session_state['modelpath']}")
    uploaded_predict_file = st.file_uploader("Choose a CSV file for prediction", type="csv", key='predict')

    if st.button('Predict') and uploaded_predict_file is not None:
        predict_df = pd.read_csv(uploaded_predict_file)
        predict_csv_data = predict_df.to_csv(index=False)

        response = requests.post(
            url="https://98db-34-106-63-144.ngrok-free.app/predict",
            data={'modelpath': st.session_state['modelpath']},
            files={'file': ('predict.csv', predict_csv_data)}
        )

        if response.status_code == 200:
            predictions = response.json()
            st.success('Prediction Successful!')
            st.write(predictions)
        else:
            st.error('Prediction failed')
            st.write(response.text)
