FROM node:alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile

ARG BUILD=production

ENV NODE_OPTIONS=--openssl-legacy-provider
COPY . .
COPY ./.env.${BUILD} ./.env
RUN npm run build:no-tsc

FROM nginx

COPY --from=builder /app/dist/ /usr/share/nginx/html
COPY ./default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]