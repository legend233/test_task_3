FROM python:alpine3.17
LABEL authors="Yuriy Choba"
RUN apk update && apk upgrade && apk add git && apk add bash
RUN pip install --upgrade pip
WORKDIR /app_db
RUN ["mkdir", "/DB"]
COPY ./main.py .
COPY ./settings.py .
COPY ./functions.py .
COPY ./schemes.py .
COPY ./requirements.txt .
ENV DB=/DB
RUN apk add --no-cache tzdata
ENV TZ Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]