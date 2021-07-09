FROM python:3.9.5-buster

COPY ./src /src

WORKDIR /src

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3","/src/initial_book_insert.py"]