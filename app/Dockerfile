FROM python:latest
RUN mkdir -p /opt/subash
WORKDIR /opt/application
RUN wget  https://jdbc.postgresql.org/download/postgresql-42.2.5.jar
RUN apt-get update
RUN apt-get install default-jdk -y
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY collect_tweets_stream.py collect_tweets_stream.py
COPY postgres/ postgres/ 
COPY credentials.json credentials.json
COPY docker-entrypoint.bash docker-entrypoint.bash
ENTRYPOINT ["bash","docker-entrypoint.bash"]
