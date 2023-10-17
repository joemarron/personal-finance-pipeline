FROM apache/airflow:2.0.2
COPY requirements.txt /requirements.txt
COPY root.crt /root.crt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt


