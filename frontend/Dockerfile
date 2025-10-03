# Stage 1: Build the Vue app
FROM node:18-alpine as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN vite build

# Stage 2: Serve with nginx
FROM nginx:alpine as production-stage

# Копируем собранное приложение в nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Копируем кастомную nginx конфигурацию (опционально)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
