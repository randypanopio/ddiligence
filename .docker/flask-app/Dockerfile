# Dockerfile for building flask backend(in .docker/flask-app/)
# Python base image (ubuntu?)
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Copy all files and directories from app_flask
COPY . .  

# Install dependencies
RUN pip install -r requirements.txt  

# Expose port 5000 (default Flask port)
EXPOSE 5000  

# Command to run the Flask app
CMD ["python", "app.py"]  


# build commands
# cd to diligence/app_flask
# run:
# docker build -t ddiligence/flask-service:0.0.1.RELEASE . -f ../.docker/flask-app/Dockerfile

# TODO use ENV vars, this image gets built with a copy of secrets.. NOT GOOD!

# SSHing to EC2 instance:
# ssh -i <your_pem_key_file> ec2-user@<public_dns_name_or_ip>