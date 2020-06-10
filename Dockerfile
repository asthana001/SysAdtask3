FROM ubuntu

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y
RUN apt-get install python3 -y

WORKDIR /root/

COPY ./server.py /root/

ENTRYPOINT ["python3.8", "/root/server.py"]

