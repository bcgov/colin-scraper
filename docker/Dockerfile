FROM python:3.10.10-bullseye

# set environment variables

# Other constants
ARG TEST_ORG_NUM='BC0990639'

# Other constants
ENV TEST_ORG_NUM=${TEST_ORG_NUM}

RUN mkdir /app
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install . 

# install Oracle Instant Client
ARG CONFIG_PATH=/app/config/tnsnames.ora
RUN apt-get update && apt-get install -y --no-install-recommends alien libaio1 wget && \
    alien -i instant-client-installs/oracle-instantclient-basic-21.9.0.0.0-1.el8.x86_64.rpm && \
    alien -i instant-client-installs/oracle-instantclient-basic-21.9.0.0.0-1.x86_64.rpm && \
    cp ${CONFIG_PATH} $/usr/lib/oracle/21/client64/lib/network/admin

ENV LD_LIBRARY_PATH="/usr/lib/oracle/21/client64/lib:${LD_LIBRARY_PATH}"
ENV TNS_ADMIN="/usr/lib/oracle/21/client64/lib/network/admin:${TNS_ADMIN}"
ENV CONFIG_PATH=${CONFIG_PATH}

# install chromedriver
ARG CHROMEDRIVER_DIR /usr/local/bin

RUN apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d ${CHROMEDRIVER_DIR}

EXPOSE 3000

ENV PYTHONPATH=/app
ENV PATH ${CHROMEDRIVER_DIR}:$PATH
ENV DRIVER_PATH=${CHROMEDRIVER_DIR}
ENV TEMP_BASE_PATH=/test-outputs

CMD ["python", "./main.py"]
