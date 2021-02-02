FROM python:3.9.1
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY wekan_ical_server.py wekan_ical_server.py
CMD python wekan_ical_server.py