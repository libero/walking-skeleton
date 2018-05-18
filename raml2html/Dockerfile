FROM node:10.1.0

RUN mkdir /api

WORKDIR /raml2html
ENV PATH /raml2html/node_modules/.bin/:$PATH

COPY package.json package-lock.json ./
RUN npm install && \
    npm cache clean --force

EXPOSE 8080

CMD rm -rf /public && cp --recursive /api /public/ && node_modules/.bin/raml2html /public/api.raml > /public/index.html && node_modules/.bin/http-server /public
