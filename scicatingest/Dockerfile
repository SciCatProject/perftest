FROM node:12


ENV http_proxy="http://10.0.0.160:8123"
WORKDIR /usr/src/app/
COPY scicatingest/package.json /usr/src/app/
COPY scicatingest/ingest.ts /usr/src/app/
COPY scicatingest/run.sh /usr/src/app/

RUN npm install
