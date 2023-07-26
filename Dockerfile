# syntax=docker/dockerfile:1

#Set a base image
FROM python:3.8-alpine

#Expose port 5000
EXPOSE 5000/tcp

#Update pip to minimize dependency errors
WORKDIR /app

#Copy dependencies file to working directory
COPY requirements.txt .

#Upgrade pip and install all dependencies in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Copy content of local dir to working directory
COPY . .

#Command to run container
CMD [ "python", "./application.py" ]
