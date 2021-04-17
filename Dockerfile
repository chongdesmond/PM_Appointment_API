#Use the Python3.6 image
FROM tiangolo/uwsgi-nginx-flask:python3.7

# Set the working directory to /app
WORKDIR /app

# Copy server configurations
COPY nginx.conf .
COPY uwsgi.ini .

# Copy requirements.txt first to utilise cache
COPY ./app/requirements.txt .

# Install the dependencies
#RUN pip install --upgrade certifi
RUN apt-get update
RUN apt-get install ca-certificates -y
RUN update-ca-certificates
RUN export SSL_CERT_DIR=/etc/ssl/certs
RUN pip install -r requirements.txt


# Copy the current directory contents into the container at /app
COPY ./app .
