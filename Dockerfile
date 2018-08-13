FROM python:2

WORKDIR /usr/src

RUN git clone https://github.com/Manuel83/craftbeerpi3.git 

WORKDIR craftbeerpi3

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/craftbeerpi3/modules/plugins/cbpi_alarm_clock
