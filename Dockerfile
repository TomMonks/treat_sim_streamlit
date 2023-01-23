FROM python:3.8-slim

# streamlit working dir
RUN mkdir /app
WORKDIR /app

# install a few essential as this is the slim build. 
# Git means we can clone from a repo instead of local copy if needed. 
# curl to perform health check
# Clean up after. 
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# copy everything including the pip requirements file 
COPY . /app

# pip install the requirements 
RUN pip3 install -r requirements.txt

# EXPOSE PORT 8501 - standard for streamlit.
EXPOSE 8501

# check the app is operating normally. 
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# run app on 0.0.0.0:8501
ENTRYPOINT ["streamlit", "run", "Overview.py", "--server.port=8501", "--server.address-0.0.0.0"]

