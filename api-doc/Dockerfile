FROM node:10.1.0

WORKDIR /raml2html

COPY package.json package-lock.json ./
RUN npm install && \
    npm cache clean --force

COPY api.raml /public/

EXPOSE 8080

CMD (node_modules/.bin/http-server -p 8087 --proxy=http://schemas:80/ &) && node_modules/.bin/raml2html /public/api.raml > /public/index.html && node_modules/.bin/http-server /public
