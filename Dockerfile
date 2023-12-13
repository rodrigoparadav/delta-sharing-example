FROM python:3.10

RUN apt-get -y update
RUN apt-get install -y unixodbc-dev
RUN apt-get -y install cmake gcc g++ build-essential

# Application base files.
COPY . /app/

# Install additional wheel libraries (if necessary).
RUN pip install pipenv
RUN pip install pipenv==2022.3.28

WORKDIR /app

# Install dependencies.
RUN cd /app/ && python setup.py install

# Variable definitions.
ENV PYTHONPATH=/app
ENV APP_ENV=dev
ENV DEBUG=True
