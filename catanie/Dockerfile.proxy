FROM node:10-alpine

ENV http_proxy "http://192.168.1.1:8123"
ENV https_proxy $http_proxy
RUN apk update && \
    apk add git 

WORKDIR /var/catanie
COPY catanie .
RUN npm i --no-cache

ENTRYPOINT ["npm", "run", "ng"]
CMD ["serve","--","--configuration", "v20"]
