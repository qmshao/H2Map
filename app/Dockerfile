FROM python:3
COPY . /appdocker
WORKDIR /appdocker
RUN pip install -r requirements.txt
CMD ["gunicorn", "--workers=3", "-b", ":3800", "map:server"]