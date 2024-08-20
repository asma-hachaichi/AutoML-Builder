# AutoML API with Queue Management

## Overview

This project provides an **AutoML API** built using **H2O.ai** and **FastAPI**.
The API supports training models asynchronously, monitors their status, and makes predictions on new data using the trained models.
The system employs **queue management** to handle model training requests, ensuring each task is processed in order (FIFO: First-In-First-Out).
The interface for interacting with the API is implemented using **Streamlit**.

## Features

- **Model Training**: Accepts a CSV file as input, automatically preprocesses the data, and trains an H2O AutoML model.
- **Task Queue Management**: Ensures that model training tasks are handled sequentially. Each task is assigned a unique `task_id` and processed in the order they are received.
- **Monitor Training Status**: Allows users to check the status of their model training task.
- **Make Predictions**: Once a model has finished training, users can upload new data for predictions.

## Technologies Used

- **H2O.ai**: For automated machine learning model training.
- **FastAPI**: For building the REST API.
- **Streamlit**: For the frontend user interface.
- **Uvicorn**: For ASGI server management.
- **PyNgrok**: For exposing the FastAPI application to the internet.
- **Python's `sched` and `asyncio`**: For managing asynchronous tasks in a queue.
- **Pandas**: For data manipulation.
- **UUID**: For generating unique task identifiers.

---

## How to Run the Project

### Backend Setup (FastAPI + H2O + Uvicorn)

1. **Install dependencies:**
   Install the required Python packages by running the following code cell in the notebook autoML_builder.ipynb :

   ```bash
   !pip install fastapi uvicorn h2o pandas requests python-multipart pyngrok
   ```

2. **Create an Ngrok Profile:**
   To use Ngrok for exposing your local server, you need to create an Ngrok account and set up a profile.
   Once signed up, you'll receive an authentication token. Add this token in the second cell of the notebook :

   ```bash
   !ngrok authtoken 'YOUR_NGROK_AUTHTOKEN'
   ```

   This will allow you to create secure tunnels for your FastAPI application.

3. **Run the FastAPI Application:**
   Instead of running the FastAPI application via a Python file, simply execute the cells of the notebook autoML_builder.ipynb.
   This notebook contains all the necessary logic for model training, task monitoring, and predictions.

   When the application starts, you will see a public Ngrok URL in the last cell's output:

   ```bash
   Public URL: https://<your-ngrok-url>.ngrok-free.app
   ```

4. **API Endpoints:**
   - **Train Model**: `POST /train`
     - Input: CSV file (multipart/form-data)
     - Output: A unique `task_id` for monitoring the task status.
   - **Monitor Task**: `GET /monitor/{task_id}`
     - Input: `task_id` (path parameter)
     - Output: Task status (waiting, in_progress, done, error) and model metrics if training is complete.
   - **Make Predictions**: `POST /predict`
     - Input: `task_id` (form data), CSV file for predictions (multipart/form-data)
     - Output: JSON predictions for the uploaded dataset.

### Frontend Setup (Streamlit)

1. **Install dependencies for Streamlit**:

   ```bash
   pip install streamlit
   ```

2. **Run the Streamlit Interface**:
   You can run the Streamlit app with the following command:

   ```bash
   streamlit run app.py
   ```

   Before running the app, make sure to paste the Ngrok URL obtained from the notebook's cell output into the BASE_URL variable in app.py.
   This URL will be used to connect the Streamlit frontend to the FastAPI backend.

3. **Interface Tabs**:
   - **Train Model**: Upload a CSV file to train a new model.
   - **Monitor Training**: Enter the `task_id` to check the training progress.
   - **Make Predictions**: After training, use the `task_id` and upload a CSV file for predictions.

---

## Detailed Explanation

### 1. Queue Management

- **Task Queue**: The backend uses an in-memory queue (`tasks` dictionary) to manage tasks. When a training request is made, it is assigned a unique `task_id` using `uuid.uuid4()`. Each task is added to the queue with an initial status of `waiting`.
- **Scheduler**: We use Python’s `sched.scheduler` to manage the execution of tasks. Each task is scheduled with a delay of `0`, ensuring that tasks are processed as soon as possible but still maintaining a First-In-First-Out (FIFO) order. The scheduler is run in a separate asyncio task, allowing the main FastAPI thread to handle other requests while tasks are being processed.

- **Asyncio**: The `asyncio.create_task()` function ensures that the task scheduling is non-blocking. This is essential for handling multiple simultaneous API requests without freezing the server.

### 2. Model Training

- **Data Preprocessing**: Before training, the system limits the number of rows in the dataset to `500` to reduce training time. This is done using a simple sampling method (`limit_rows` function).

- **H2O AutoML**: The API uses H2O’s `AutoML` for model training. By default, the system trains models using three algorithms (`GLM`, `GBM`, `XGBoost`). If the performance of the model is unsatisfactory based on predefined metrics (logloss for classification, R² for regression), the system may include Deep Learning models in the training.

- **Model Saving**: Once a model is trained, it is saved, and its path is stored in the task's `model_details` dictionary along with the relevant metrics (`AUC`, `MSE`, `logloss`... ).

### 3. Task Monitoring

- **Monitor Status**: The `monitor_task` endpoint allows the client to check the status of their task using the `task_id`. The task's status is updated as it progresses from `waiting` to `in_progress`, then to `done` or `error`.

### 4. Prediction

- **Prediction API**: Once a model is successfully trained, the user can make predictions by providing the `task_id` and a new CSV file for prediction. The API loads the previously saved model and makes predictions on the new data, returning the results as a JSON response.

---

## Streamlit Interface

- **Train Model**: In the "Train Model" tab, upload a CSV file and click "Train Model". The `task_id` will be displayed once training starts.
- **Monitor Training**: In the "Monitor Training" tab, input the `task_id` and click "Check Status" to see if your model has finished training.
- **Make Predictions**: In the "Make Predictions" tab, input the `task_id` and upload a CSV file for predictions. The results will be displayed in a table format.

---

## Notes

- This implementation uses **in-memory storage for tasks**, which means all task data will be lost when the server restarts.
- The **queue management** system ensures that model training tasks are handled sequentially.
