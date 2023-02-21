FROM python:3.10.10-bullseye

# set environment variables

# Oracle DB
ARG ORACLE_DB_USERNAME="readonly"
ARG ORACLE_DB_PASSWORD="t3mpt3mp"
ARG ORACLE_DB_DSN="cprd.world"

# Other constants
ARG TEST_ORG_NUM='BC0990639'
ARG DATE_RANGE_START="2002/01/01"
ARG DATE_RANGE_END="2003/01/01"
ARG FINAL_END_DATE="2023/01/05"

# Oracle DB
ENV ORACLE_DB_USERNAME=${ORACLE_DB_USERNAME}
ENV ORACLE_DB_PASSWORD=${ORACLE_DB_PASSWORD}
ENV ORACLE_DB_DSN=${ORACLE_DB_DSN}

# Other constants
ENV TEST_ORG_NUM=${TEST_ORG_NUM}
ENV DATE_RANGE_START=${DATE_RANGE_START}
ENV DATE_RANGE_END=${DATE_RANGE_END}
ENV FINAL_END_DATE=${FINAL_END_DATE}

RUN mkdir /app
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install . 

# install Oracle Instant Client
RUN apt-get update && apt-get install -y --no-install-recommends alien libaio1 wget && \
    wget https://download.oracle.com/otn_software/linux/instantclient/219000/oracle-instantclient-basic-21.9.0.0.0-1.el8.x86_64.rpm && \
    wget https://download.oracle.com/otn_software/linux/instantclient/219000/oracle-instantclient-basic-21.9.0.0.0-1.x86_64.rpm && \
    alien -i oracle-instantclient-basic-21.9.0.0.0-1.el8.x86_64.rpm && \
    alien -i oracle-instantclient-basic-21.9.0.0.0-1.x86_64.rpm && \
    cp /app/config/tnsnames.ora /usr/lib/oracle/21/client64/lib/network/admin
    
ENV LD_LIBRARY_PATH="/usr/lib/oracle/21/client64/lib:${LD_LIBRARY_PATH}"
ENV TNS_ADMIN="/usr/lib/oracle/21/client64/lib/network/admin:${TNS_ADMIN}"

# install google chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb

# install chromedriver
RUN apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /app/chrome-web-driver

EXPOSE 3000

ENV PYTHONPATH=/app
CMD ["python", "main.py"]
