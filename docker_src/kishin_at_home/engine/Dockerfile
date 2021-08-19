FROM python:3.9.5-buster

COPY ./src /src


WORKDIR /src

CMD ["bash","/src/init.sh"]

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

WORKDIR /src/shogi_dir

CMD ["python3","yaneura_driver.py"]