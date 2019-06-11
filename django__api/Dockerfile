FROM python:3.6

MAINTAINER James Ward

# Basic setup
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install libgdal-dev
RUN mkdir -p /usr/src/app
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

# Cron job files
RUN apt-get install -y cron
ADD crontab /etc/cron.d/crontab
ADD process_task_script.sh /process_task_script.sh
RUN touch /var/log/cron.log
COPY entry.sh /entry.sh
RUN chmod 755 /process_task_script.sh /entry.sh
RUN service cron start
RUN crontab /etc/cron.d/crontab

# Install requirements and create app directory
COPY requirements.txt /usr/src/app
COPY . /usr/src/app
COPY start_app.sh /start_app.sh

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
