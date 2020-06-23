FROM python:3-alpine

# installing Build & Runtime libraries
RUN apk add build-base jpeg-dev zlib-dev libx11-dev libpng-dev libxcursor-dev 

# Add requirements.txt before rest of repo for caching
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt && ls

ADD . /app

# Build App
RUN python setup.py install sdist bdist_wheel


# Install App 
RUN cd ./dist && pip install clickgen-*.tar.gz
WORKDIR /

# Clean Up build libraries
RUN apk del build-base

# Remove code 
RUN rm -rf /app
