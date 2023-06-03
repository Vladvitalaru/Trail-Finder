# syntax=docker/dockerfile:1
#init a base image
FROM python:3.10-slim-bullseye

#Update pip to minimize dependency errors

WORKDIR /python-docker

COPY requirements.txt requirements.txt

#Upgrade pip and install all dependencies in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Expose port 5000
EXPOSE 5000 

COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=5.0.0.6"]
CMD python ./server_whoosh.py
