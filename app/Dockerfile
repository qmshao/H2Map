FROM python:3
COPY . /appdocker
WORKDIR /appdocker
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["map.py"]