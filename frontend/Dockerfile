# Build asamasi
FROM node:18-alpine AS builder

WORKDIR /app

# Bagimliliklari kopyala ve yukle
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Kaynak kodlari kopyala
COPY . .

# Build
ENV REACT_APP_API_URL=/api/v1
RUN yarn build

# Production asamasi
FROM nginx:alpine

# Nginx yapilandirmasi
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
