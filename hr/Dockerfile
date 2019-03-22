FROM python:3.7
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN pip install scrapy
CMD [ "scrapy","crawl", "jobs"]