# install base image for debian 9
FROM ubuntu:18.04 # OS 이미지 다운로드 및 실행
ENV TZ=US/Central # OS에 TIMEZONE 설정 -> 꼭 필요
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >
/etc/timezone
# 필요한 package들 모두 설치한다(OS에 설치해야 할 패키지들)
RUN apt-get update \
 && apt-get install tesseract-ocr -y
RUN tesseract -v
# 로컬에 있는 코드들 (requirements.txt나 main.py 등등)을 ubuntu os에 복사
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
# 필요한 python 라이브러리들을 설치한다(requirements.txt)
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENV FLASK_APP=main.py
# flask에서 사용할 port 지정
EXPOSE 8080
# gunicorn은 python wsgi http server이다. 한번에 8명을 동시에 받을 수 있다
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 30 main:app