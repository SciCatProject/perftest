FROM node:12


ENV http_proxy "http://192.168.1.1:8123"
ENV https_proxy $http_proxy
WORKDIR /usr/src/app/
COPY scicatingest/package.json /usr/src/app/
COPY scicatingest/ingest.ts /usr/src/app/
COPY scicatingest/run.sh /usr/src/app/

RUN npm install
CMD ["./run.sh"]
