FROM apache/airflow:2.0.1-python3.6

LABEL version="0.1"
WORKDIR ${AIRFLOW_HOME}

COPY dags/ ${AIRFLOW_HOME}/dags
COPY requirements.txt ${AIRFLOW_HOME}

RUN ["python", "-m", "pip", "install", "--user", "--upgrade", "pip"]
RUN ["pip", "install", "-r", "requirements.txt"]

# COPY unittests.cfg ${AIRFLOW_HOME}/unittests.cfg
# COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
# COPY unittests/ ${AIRFLOW_HOME}/unittests
# COPY integrationtests ${AIRFLOW_HOME}/integrationtests