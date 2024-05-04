FROM apache/airflow:2.2.3
ENV AIRFLOW_HOME=/opt/airflow
USER root

# Install necessary dependencies
RUN apt-get update -qq && apt-get install -qqq \
    vim \
    git \
    gcc \
    g++

# Copy the required code files into the container
COPY ../app /opt/airflow/app
COPY ../requirements.txt /opt/airflow/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID