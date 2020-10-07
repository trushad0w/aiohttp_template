FROM python:3.7

COPY requirements requirements

RUN pip3 install -r requirements && rm requirements

COPY . app

WORKDIR app

EXPOSE 8000
