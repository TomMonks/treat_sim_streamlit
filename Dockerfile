FROM python:3.8-slim

# ? group and user for app
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 -ms /bin/bash appuser

# install pipp and virtual environment
RUN pip3 install --no-cache-dir --upgrade \
    pip \
    virtualenv

# install a few essentials as this is the slim build. 
# Git means we can clone from a repo instead of local copy if needed. 
# curl to perform health check
# Clean up after. 
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# swith user and working dir
USER appuser
WORKDIR /home/appuser

# clone the repo into app directory
RUN git clone https://github.com/TomMonks/treat_sim_streamlit app

# activate virtual env
ENV VIRTUAL_ENV=/home/appuser/venv
RUN virtualenv ${VIRTUAL_ENV}
RUN . ${VIRTUAL_ENV}/bin/activate && pip install -r app/requirements.txt

# EXPOSE PORT 8501 - standard for streamlit.
EXPOSE 8501

COPY run.sh /home/appuser

