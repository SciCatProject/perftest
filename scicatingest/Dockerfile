FROM node:12

WORKDIR /usr/src/app/
COPY scicatingest/package.json /usr/src/app/
COPY scicatingest/ingest.ts /usr/src/app/

RUN npm install

RUN npx ts-node  ./ingest.ts