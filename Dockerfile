FROM python:3.12.7

WORKDIR /home_helper

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt ruff pre-commit

COPY . .

COPY wait-for-it.sh /usr/bin/wait-for-it.sh
RUN chmod +x /usr/bin/wait-for-it.sh
