# install base image for debian 9
FROM ubuntu:18.04
ENV TZ=US/Central
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV PORT = 8080
#ENV FLASK_APP=hello.py

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# install tesseract-ocr
RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    python3 \
    python3-pip \
    python3-opencv \
    python-enchant \
    && apt-get clean \
    && apt-get autoremove

RUN tesseract -v

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -c "import nltk; nltk.download('punkt')"

ENV FLASK_APP=main.py

RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8

VOLUME ["/data"]
EXPOSE 8080

#CMD ["python3", "main.py"]
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 30 main:app
