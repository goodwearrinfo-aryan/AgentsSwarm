# Stage 1: Build the React application
FROM node:20-alpine AS build

WORKDIR /app

# Build arg for VITE_APP_URL (required by generate-cli.js prebuild script)
ARG VITE_APP_URL=https://agents-swarm.local
ENV VITE_APP_URL=${VITE_APP_URL}

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve via NGINX
FROM nginx:alpine

# Copy built assets to NGINX HTML directory
COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
