FROM python:3.9.5-buster

WORKDIR /src

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3","random_requester.py"]