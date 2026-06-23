FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app + artifacts
COPY Streamlit_App /app/Streamlit_App
COPY Model /app/Model
COPY Dataset /app/Dataset
COPY Documentation /app/Documentation
COPY Notebook /app/Notebook
COPY README.md /app/README.md

EXPOSE 8501

# Streamlit expects HOST/PORT from env on many platforms
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501

CMD ["streamlit", "run", "Streamlit_App/app.py", "--server.address=0.0.0.0", "--server.port=8501"]

