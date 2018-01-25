FROM ubuntu:latest
MAINTAINER Ethan Wright "ewright362@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
EXPOSE 8888
EXPOSE 5000
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["StripController.py"]
