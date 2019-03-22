FROM python:3.7
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    && apt-get clean \
    && apt-get autoremove
RUN pip install -r requirements.txt

CMD [ "scrapy","crawl", "jobs" ]