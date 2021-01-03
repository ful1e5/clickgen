FROM python:3-alpine

# Installing necessary runtime libraries
RUN apk add build-base jpeg-dev zlib-dev libx11-dev libpng-dev libxcursor-dev 

# For caching
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ADD . /app

# Building app
RUN python setup.py install sdist bdist_wheel
RUN cd ./dist && pip install clickgen-*.tar.gz


# Cleaning build libraries
WORKDIR /
RUN apk del build-base
RUN rm -rf /app
