FROM python:3.6-slim
#First installs linux Ubuntu and then downloads and installs python on top of it.

WORKDIR /app
#roughly the equivalent of mkdir app upon creation of the container

ADD . /app
#copy all files (e.g. app.py, Dockerfile, reuqirments.txt and move into /app)

RUN pip install --trusted-host pypi.python.org -r requirements.txt
#install all python libraries that you find in the file called requirements.txt

CMD ["python", "etl.py"]
#run the source code
