FROM ubuntu
COPY align.py align.py
RUN chmod +x align.py
RUN apt update
RUN apt install -y bwa
RUN apt install -y python3
