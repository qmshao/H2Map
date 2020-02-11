FROM debian:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /appdocker
WORKDIR /appdocker
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["map.py"]