FROM python:3.6

MAINTAINER James Ward

RUN apt-get -y update
RUN apt-get -y upgrade
RUN mkdir -p /usr/src/app

COPY requirements.txt /usr/src/app
COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install scikit-surprise
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
