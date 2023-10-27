FROM python:alpine3.17
LABEL authors="Yuriy Choba"
RUN apk update && apk upgrade && apk add git && apk add bash
RUN pip install --upgrade pip
WORKDIR /app_client
RUN ["mkdir", "/output"]
COPY ./main.py .
COPY ./settings.py .
COPY ./functions.py .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV SERVER=localhost
ENV PORT=8000
ENV OUTPUTFOLDER=/output/
RUN apk add --no-cache tzdata
ENV TZ Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENTRYPOINT ["python", "main.py"]