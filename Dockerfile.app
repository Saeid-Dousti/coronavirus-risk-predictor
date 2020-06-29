# Dockerfile for building streamline app

# pull miniconda image
FROM continuumio/miniconda3

# copy local files into container
COPY corona_predict.py /tmp/
COPY requirements.txt /tmp/
COPY app /tmp/app
COPY configs tmp/configs
COPY data tmp/data
COPY static tmp/static

# .streamlit for something to do with making enableCORS=False
COPY .streamlit /tmp/.streamlit

# install python 3.8.3
RUN conda install python=3.8.3

ENV PORT 8080
# ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/build/storage-read-only-service-account.json

# change directory
WORKDIR /tmp

# install dependencies
RUN apt-get update && apt-get install -y vim g++
RUN pip install -r requirements.txt

# run commands
CMD ["streamlit", "run", "corona_predict.py"]